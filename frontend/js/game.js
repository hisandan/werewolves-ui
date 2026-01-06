class WerewolfGame {
    constructor() {
        this.players = [];
        this.phase = 'night';
        this.round = 1;
        this.ws = null;

        this.init();
    }

    init() {
        this.connectWebSocket();
        this.bindEvents();
    }

    connectWebSocket() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//localhost:8000/ws`;
        this.ws = new WebSocket(wsUrl);

        this.ws.onopen = () => {
            console.log('Connected to backend');
            this.addEvent('system', 'Connected to Game Server');
            document.querySelector('.phase-badge').style.borderColor = '#22c55e'; // Green pulse
        };

        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleServerMessage(data);
        };

        this.ws.onclose = () => {
            console.log('Disconnected');
            this.addEvent('system', 'Disconnected from server');
            document.querySelector('.phase-badge').style.borderColor = '#ef4444'; // Red pulse
            setTimeout(() => this.connectWebSocket(), 3000);
        };
    }

    handleServerMessage(msg) {
        console.log('Received:', msg);
        switch (msg.type) {
            case 'game_start':
                this.setupPlayers(msg.payload.players, msg.payload.roles);
                this.resetUI();
                break;
            case 'phase_change':
                this.setPhase(msg.payload.phase);
                this.round = msg.payload.round;
                document.getElementById('roundDisplay').textContent = this.round;
                this.addEvent('system', `Phase Change: ${msg.payload.phase.toUpperCase()} (Round ${this.round})`);
                break;
            case 'player_speak':
                this.addDebateMessage(msg.payload.player_id, msg.payload.content);
                break;
            case 'player_eliminated':
                this.killPlayer(msg.payload.player_id, msg.payload.role);
                break;
            case 'game_over':
                this.showVictory(msg.payload.winner, msg.payload.scores);
                break;
            case 'system_error':
                console.error('System Error:', msg.payload.error);
                this.addEvent('death', `SYSTEM ERROR: ${msg.payload.error}`);
                alert(`Game Error: ${msg.payload.error}`);
                break;
        }
    }

    resetUI() {
        document.getElementById('gameStatusPanel').classList.add('hidden');
        document.getElementById('debateLog').innerHTML = '';
        document.getElementById('eventLog').innerHTML = '';
        this.addEvent('system', 'Game Initialized.');
    }

    setupPlayers(playerNames, roles) {
        this.players = playerNames.map((name, i) => ({
            id: name,
            name: name,
            role: roles ? roles[name] : 'Unknown', // Roles usually hidden at start in client but available if passed
            alive: true
        }));

        const arena = document.querySelector('.arena-game');
        document.querySelectorAll('.player-node').forEach(n => n.remove());

        this.players.forEach((player, i) => {
            const node = document.createElement('div');
            node.className = 'player-node';
            node.dataset.playerId = player.id;
            node.dataset.alive = 'true';

            node.innerHTML = `
                <div class="node-avatar">
                   👤
                </div>
                <div class="node-name">${player.name}</div>
             `;

            arena.appendChild(node);
        });

        this.addEvent('system', `Game Started with ${this.players.length} players`);
        // Distribute function called via override in HTML
    }

    addDebateMessage(player, content) {
        const chat = document.getElementById('debateLog');
        const msg = document.createElement('div');
        msg.className = 'debate-msg';
        msg.innerHTML = `<span class="msg-author">${player}</span><span class="msg-text">${content}</span>`;
        chat.appendChild(msg);
        chat.scrollTop = chat.scrollHeight;

        // Highlight speaker
        const node = document.querySelector(`.player-node[data-playerId="${player}"]`);
        if (node) {
            node.classList.add('speaking');
            setTimeout(() => node.classList.remove('speaking'), 2500);
        }
    }

    killPlayer(playerId, role) {
        const player = this.players.find(p => p.id === playerId);
        if (player) {
            player.alive = false;
            const node = document.querySelector(`.player-node[data-playerId="${playerId}"]`);
            if (node) node.dataset.alive = 'false';
            this.addEvent('death', `${player.name} died! Role was: ${role || 'Unknown'}`);

            // Show skull
            if (node) node.querySelector('.node-avatar').textContent = '💀';
        }
    }

    setPhase(phase) {
        this.phase = phase;
        const display = document.getElementById('phaseDisplay');
        display.textContent = phase.toUpperCase();

        const badge = document.querySelector('.phase-badge');
        if (phase === 'night') {
            badge.style.background = '#1e1b4b'; // Dark blue
        } else {
            badge.style.background = '#fff7ed'; // Light orange
            badge.style.color = '#333';
        }

        window.werewolfAudio?.playSound('phase');
    }

    showVictory(winner, scores) {
        const panel = document.getElementById('gameStatusPanel');
        panel.classList.remove('hidden');

        document.getElementById('winnerDisplay').textContent = `${winner.toUpperCase()} WIN!`;

        // Populate Role Reveal
        const roleList = document.getElementById('roleList');
        roleList.innerHTML = '';

        if (scores && Array.isArray(scores)) {
            scores.forEach(score => {
                const item = document.createElement('div');
                item.className = 'role-item';
                // E.g. Player_1 (Werewolf)
                item.textContent = `${score.player_name}: ${score.role}`;
                if (score.role === 'Werewolf') item.style.color = '#f87171'; // Red
                else if (score.role === 'Doctor') item.style.color = '#4ade80'; // Green
                else if (score.role === 'Seer') item.style.color = '#c084fc'; // Purple
                roleList.appendChild(item);
            });
        }

        window.werewolfAudio?.playSound('victory');
    }

    addEvent(type, text) {
        const log = document.getElementById('eventLog');
        const event = document.createElement('div');
        event.className = `event event-${type}`;
        event.innerHTML = text;
        log.appendChild(event);
        log.scrollTop = log.scrollHeight;
    }

    bindEvents() {
        document.getElementById('startBtn')?.addEventListener('click', () => this.startGame());
    }

    async startGame() {
        const numPlayers = document.getElementById('playerCount').value;
        try {
            this.addEvent('system', 'Initializing new simulation...');
            await fetch('http://localhost:8000/start_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ num_players: parseInt(numPlayers) })
            });
        } catch (e) {
            console.error('Failed to start game', e);
            this.addEvent('system', 'Error starting game. Check backend console.');
        }
    }
}

window.game = new WerewolfGame();
