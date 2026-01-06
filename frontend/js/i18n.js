const translations = {
    es: {
        nav_about: "Sobre",
        nav_roles: "Roles",
        nav_metrics: "Métricas",
        nav_settings: "Configuración",
        nav_start: "Iniciar Juego",
        hero_line1: "La Noche Cae.",
        hero_line2: "Los Lobos Despiertan.",
        hero_subtitle: "Un benchmark de IA para evaluar deducción social, razonamiento estratégico y capacidad de engaño.",
        btn_start: "Comenzar Partida",
        btn_github: "GitHub",
        about_title: "¿Qué es Werewolf Arena?",
        card_benchmark_title: "Benchmark de IA",
        card_benchmark_desc: "Evalúa agentes de IA en habilidades sociales complejas.",
        card_deduction_title: "Deducción Social",
        card_deduction_desc: "Los agentes identifican roles mediante análisis de comportamiento.",
        card_deception_title: "Engaño",
        card_deception_desc: "Los lobos ocultan su identidad. Los aldeanos buscan la verdad.",
        card_metrics_title: "Métricas",
        card_metrics_desc: "Win rate, supervivencia y precisión.",
        roles_title: "Roles del Juego",
        role_werewolf: "Hombre Lobo",
        role_werewolf_desc: "Elimina cada noche. Engaña de día.",
        role_seer: "Vidente",
        role_seer_desc: "Descubre la verdad por la noche.",
        role_doctor: "Doctor",
        role_doctor_desc: "Protege a los inocentes.",
        role_villager: "Aldeano",
        role_villager_desc: "Vota para exiliar.",
        footer_desc: "Entorno compatible con AgentBeats y OpenAI API.",
        // Game Page
        btn_exit: "SALIR",
        lbl_round: "RONDA",
        lbl_waiting: "ESPERANDO",
        panel_agents: "AGENTES",
        btn_start_game: "INICIAR PARTIDA",
        btn_stop_game: "DETENER PARTIDA",
        stat_alive: "Vivos:",
        stat_wolves: "Lobos:",
        msg_village_sleeps: "La aldea duerme...",
        role_villagers: "ALDEANOS",
        role_werewolves: "LOBOS",
        panel_chronicles: "CRÓNICAS",
        msg_waiting_start: "Esperando inicio...",
        // Settings
        nav_home: "Inicio",
        nav_game: "Juego",
        settings_title: "Configuración LLM",
        settings_subtitle: "Selecciona el proveedor de IA",
        btn_save: "Guardar Configuración"
    },
    en: {
        nav_about: "About",
        nav_roles: "Roles",
        nav_metrics: "Metrics",
        nav_settings: "Settings",
        nav_start: "Start Game",
        hero_line1: "Night Falls.",
        hero_line2: "Wolves Awaken.",
        hero_subtitle: "An AI benchmark to evaluate social deduction, strategic reasoning, and deception skills.",
        btn_start: "Start Game",
        btn_github: "GitHub",
        about_title: "What is Werewolf Arena?",
        card_benchmark_title: "AI Benchmark",
        card_benchmark_desc: "Evaluates AI agents on complex social skills.",
        card_deduction_title: "Social Deduction",
        card_deduction_desc: "Agents identify roles via behavioral analysis.",
        card_deception_title: "Deception",
        card_deception_desc: "Wolves hide their identity. Villagers seek truth.",
        card_metrics_title: "Metrics",
        card_metrics_desc: "Win rate, survival, and accuracy.",
        roles_title: "Game Roles",
        role_werewolf: "Werewolf",
        role_werewolf_desc: "Eliminates at night. Deceives by day.",
        role_seer: "Seer",
        role_seer_desc: "Uncovers truth at night.",
        role_doctor: "Doctor",
        role_doctor_desc: "Protects the innocent.",
        role_villager: "Villager",
        role_villager_desc: "Votes to exile suspects.",
        footer_desc: "Environment compatible with AgentBeats and OpenAI API.",
        // Game Page
        btn_exit: "EXIT",
        lbl_round: "ROUND",
        lbl_waiting: "WAITING",
        panel_agents: "AGENTS",
        btn_start_game: "START GAME",
        btn_stop_game: "STOP GAME",
        stat_alive: "Alive:",
        stat_wolves: "Wolves:",
        msg_village_sleeps: "The village sleeps...",
        role_villagers: "VILLAGERS",
        role_werewolves: "WEREWOLVES",
        panel_chronicles: "CHRONICLES",
        msg_waiting_start: "Waiting for start...",
        // Settings
        nav_home: "Home",
        nav_game: "Game",
        settings_title: "LLM Configuration",
        settings_subtitle: "Select AI Provider",
        btn_save: "Save Configuration"
    }
};

let currentLang = localStorage.getItem('lang') || 'es';

function setLanguage(lang) {
    currentLang = lang;
    localStorage.setItem('lang', lang);
    const elements = document.querySelectorAll('[data-i18n]');
    elements.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });

    const btn = document.getElementById('langToggle');
    if (btn) btn.innerHTML = lang === 'es' ? '🇪🇸 ES / 🇬🇧 EN' : '🇬🇧 EN / 🇪🇸 ES';
}

function toggleLanguage() {
    setLanguage(currentLang === 'es' ? 'en' : 'es');
}

// Init
document.addEventListener('DOMContentLoaded', () => setLanguage(currentLang));
