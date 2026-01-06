class WerewolfPolyphonicAudio {
    constructor() {
        this.audioContext = null;
        this.masterGain = null;
        this.musicGain = null;
        this.sfxGain = null;
        this.isEnabled = true;
        this.isMusicPlaying = false;
        this.musicInterval = null;
        this.ambientIntervals = [];

        // Configuración
        this.config = {
            masterVolume: 0.4,
            musicVolume: 0.15,
            sfxVolume: 0.3
        };

        // Escalas musicales oscuras
        this.scales = {
            minor: [0, 2, 3, 5, 7, 8, 10], // Natural minor
            phrygian: [0, 1, 3, 5, 7, 8, 10], // Modo frigio - muy oscuro
            locrian: [0, 1, 3, 5, 6, 8, 10], // Modo locrio - el más oscuro
            harmonicMinor: [0, 2, 3, 5, 7, 8, 11] // Menor armónica - dramática
        };

        // Frecuencia base (D2)
        this.baseFreq = 73.42;

        this.init();
    }

    init() {
        // Inicializar al primer clic
        document.addEventListener('click', () => this.initAudioContext(), { once: true });
        document.addEventListener('keydown', () => this.initAudioContext(), { once: true });
    }

    initAudioContext() {
        if (this.audioContext) return;

        try {
            this.audioContext = new (window.AudioContext || window.webkitAudioContext)();

            // Crear cadena de ganancia
            this.masterGain = this.audioContext.createGain();
            this.masterGain.gain.value = this.config.masterVolume;
            this.masterGain.connect(this.audioContext.destination);

            // Canal de música
            this.musicGain = this.audioContext.createGain();
            this.musicGain.gain.value = this.config.musicVolume;
            this.musicGain.connect(this.masterGain);

            // Canal de SFX
            this.sfxGain = this.audioContext.createGain();
            this.sfxGain.gain.value = this.config.sfxVolume;
            this.sfxGain.connect(this.masterGain);

            console.log('🔊 Polyphonic Audio Engine initialized');

            // Iniciar música de fondo automáticamente
            this.startBackgroundMusic();

        } catch (e) {
            console.warn('Audio not available:', e);
        }
    }

    // ========================
    // MÚSICA DE FONDO CONTINUA
    // ========================

    startBackgroundMusic() {
        if (this.isMusicPlaying || !this.audioContext) return;
        this.isMusicPlaying = true;

        // Drone grave continuo
        this.startDrone();

        // Melodía lenta aleatoria
        this.startMelody();

        // Efectos ambientales
        this.startAmbientEffects();

        console.log('🎵 Background music started');
    }

    stopBackgroundMusic() {
        this.isMusicPlaying = false;

        // Limpiar intervalos
        this.ambientIntervals.forEach(id => clearInterval(id));
        this.ambientIntervals = [];

        if (this.musicInterval) {
            clearInterval(this.musicInterval);
            this.musicInterval = null;
        }

        console.log('🔇 Background music stopped');
    }

    startDrone() {
        if (!this.audioContext) return;

        // Crear drones graves continuos (polifónicos)
        const playDrone = () => {
            // Fundamental grave
            this.playNote(this.baseFreq, 8, 'sine', 0.04, this.musicGain);
            // Quinta justa
            this.playNote(this.baseFreq * 1.5, 8, 'sine', 0.025, this.musicGain);
            // Octava
            this.playNote(this.baseFreq * 2, 8, 'triangle', 0.015, this.musicGain);

            // Añadir algo de ruido filtrado
            this.playFilteredNoise(8, 100, 0.02, this.musicGain);
        };

        playDrone();
        this.ambientIntervals.push(setInterval(playDrone, 7500));
    }

    startMelody() {
        if (!this.audioContext) return;

        const scale = this.scales.phrygian;
        let lastNoteIndex = 0;

        const playMelodyNote = () => {
            if (!this.isMusicPlaying) return;

            // Movimiento melódico sutil
            const direction = Math.random() > 0.5 ? 1 : -1;
            const step = Math.floor(Math.random() * 3);
            lastNoteIndex = Math.max(0, Math.min(scale.length - 1, lastNoteIndex + (direction * step)));

            const semitone = scale[lastNoteIndex];
            const octave = 2 + Math.floor(Math.random() * 2); // Octavas 2-3
            const freq = this.baseFreq * Math.pow(2, octave) * Math.pow(2, semitone / 12);

            // Nota con reverb simulado
            this.playNote(freq, 2 + Math.random() * 2, 'triangle', 0.03, this.musicGain);

            // A veces tocar una segunda nota (armonía)
            if (Math.random() > 0.6) {
                const harmonyIndex = (lastNoteIndex + 2) % scale.length;
                const harmonySemitone = scale[harmonyIndex];
                const harmonyFreq = this.baseFreq * Math.pow(2, octave) * Math.pow(2, harmonySemitone / 12);
                this.playNote(harmonyFreq, 1.5, 'sine', 0.02, this.musicGain);
            }
        };

        this.musicInterval = setInterval(playMelodyNote, 3000 + Math.random() * 4000);
    }

    startAmbientEffects() {
        if (!this.audioContext) return;

        // Viento aleatorio
        const windInterval = setInterval(() => {
            if (Math.random() > 0.7 && this.isMusicPlaying) {
                this.playWind(4 + Math.random() * 3);
            }
        }, 8000);
        this.ambientIntervals.push(windInterval);

        // Crujidos aleatorios
        const creakInterval = setInterval(() => {
            if (Math.random() > 0.8 && this.isMusicPlaying) {
                this.playCreak();
            }
        }, 12000);
        this.ambientIntervals.push(creakInterval);
    }

    // ... Additional SFX methods ...

    playNote(freq, duration, type = 'sine', volume = 0.1, destination = null) {
        if (!this.audioContext) return;

        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();

        osc.type = type;
        osc.frequency.value = freq;

        gain.gain.setValueAtTime(volume, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + duration);

        osc.connect(gain);
        gain.connect(destination || this.masterGain);

        osc.start();
        osc.stop(this.audioContext.currentTime + duration);
    }

    playFilteredNoise(duration, cutoff, volume, destination) {
        if (!this.audioContext) return;

        const bufferSize = this.audioContext.sampleRate * duration;
        const buffer = this.audioContext.createBuffer(1, bufferSize, this.audioContext.sampleRate);
        const data = buffer.getChannelData(0);

        for (let i = 0; i < bufferSize; i++) {
            data[i] = Math.random() * 2 - 1;
        }

        const noise = this.audioContext.createBufferSource();
        noise.buffer = buffer;

        const filter = this.audioContext.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.value = cutoff;

        const gain = this.audioContext.createGain();
        gain.gain.setValueAtTime(volume, this.audioContext.currentTime);
        gain.gain.linearRampToValueAtTime(0, this.audioContext.currentTime + duration);

        noise.connect(filter);
        filter.connect(gain);
        gain.connect(destination || this.masterGain);

        noise.start();
    }

    playCreak() {
        if (!this.audioContext) return;
        const osc = this.audioContext.createOscillator();
        const gain = this.audioContext.createGain();
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(100 + Math.random() * 50, this.audioContext.currentTime);
        osc.frequency.linearRampToValueAtTime(60 + Math.random() * 30, this.audioContext.currentTime + 0.3);
        gain.gain.setValueAtTime(0.03, this.audioContext.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, this.audioContext.currentTime + 0.3);
        osc.connect(gain);
        gain.connect(this.musicGain);
        osc.start();
        osc.stop(this.audioContext.currentTime + 0.3);
    }

    playWind(duration) {
        this.playFilteredNoise(duration, 300, 0.05, this.musicGain);
    }

    playHover() { this.playNote(880, 0.03, 'square', 0.02, this.sfxGain); }
    playClick() { this.playNote(440, 0.05, 'square', 0.05, this.sfxGain); }
}

window.werewolfAudio = new WerewolfPolyphonicAudio();
