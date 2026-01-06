class WerewolfWS {
    constructor(url) {
        this.url = url || `ws://${window.location.hostname}:8000/ws`;
        this.socket = null;
        this.listeners = {};
        this.isConnected = false;
        this.reconnectTimer = null;
    }

    connect() {
        if (this.socket) {
            this.socket.close();
        }

        this.socket = new WebSocket(this.url);

        this.socket.onopen = () => {
            console.log('WS Connected');
            this.isConnected = true;
            this.trigger('connect');
            this.updateStatus('Connected', 'active');
        };

        this.socket.onclose = () => {
            console.log('WS Disconnected');
            this.isConnected = false;
            this.trigger('disconnect');
            this.updateStatus('Disconnected', 'inactive');
            // Auto reconnect
            clearTimeout(this.reconnectTimer);
            this.reconnectTimer = setTimeout(() => this.connect(), 3000);
        };

        this.socket.onerror = (err) => {
            console.error('WS Error', err);
        };

        this.socket.onmessage = (msg) => {
            try {
                const data = JSON.parse(msg.data);
                this.trigger(data.type, data.payload);
                this.trigger('any', data); // Catch-all
            } catch (e) {
                console.error('WS Parse Error', e);
            }
        };
    }

    on(event, callback) {
        if (!this.listeners[event]) this.listeners[event] = [];
        this.listeners[event].push(callback);
    }

    trigger(event, data) {
        if (this.listeners[event]) {
            this.listeners[event].forEach(cb => cb(data));
        }
    }

    updateStatus(text, statusClass) {
        const el = document.getElementById('wsStatus');
        if (el) {
            el.textContent = text;
            el.className = `connection-status-pill ${statusClass}`;
        }
    }

    send(type, payload) {
        if (this.isConnected) {
            this.socket.send(JSON.stringify({ type, payload }));
        }
    }
}

// Global instance
window.werewolfWS = new WerewolfWS();
