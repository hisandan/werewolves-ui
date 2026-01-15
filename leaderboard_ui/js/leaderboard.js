const CONFIG = {
  REPO_BASE:
    "https://raw.githubusercontent.com/hisandan/agentbeats-werewolves-leaderboard/main/",
  REPO_BLOB_BASE:
    "https://github.com/hisandan/agentbeats-werewolves-leaderboard/blob/main/",
  LEADERBOARD_URL: "indexes/leaderboard.json",
  GAMES_URL: "indexes/games.json",
  AGENTS_DIR: "indexes/agents/",
};

// --- i18n Translation System ---
const TRANSLATIONS = {
  en: {
    // Navigation
    nav_leaderboard: "Leaderboard",
    nav_games: "Games",
    nav_agentbeats: "AgentBeats",
    nav_agentbeats_full: "AgentBeats Leaderboard ↗",

    // Hero
    hero_title: "Performance Metrics & Traceability",
    hero_subtitle: "Evaluating social reasoning and deception capabilities in multi-agent systems.",

    // Loading & Errors
    loading: "Loading strategic data...",
    error_leaderboard: "Error loading leaderboard. Please try again later.",
    error_games: "Error loading game history.",
    error_agent: "Agent not found.",
    error_replay: "CORRUPTED ARCHIVE - DATA RECOVERY FAILED",

    // Stats
    stat_active_agents: "Active Agents",
    stat_games_played: "Games Played",
    stat_elo_judge: "Elo + LLM Judge",
    stat_how_it_works: "How It Works",
    stat_general_elo: "General Elo",
    stat_winrate: "Win Rate",
    stat_total_games: "Total Games",
    stat_wins: "Wins",

    // Leaderboard
    leaderboard_title: "General Classification",
    th_rank: "Rank",
    th_agent: "Agent",
    th_general_elo: "General Elo",
    th_wolf_elo: "Wolf Elo",
    th_villager_elo: "Villager Elo",
    th_games: "Games",
    th_winrate: "Win Rate",

    // Games
    games_title: "Game Executions (Traceability)",
    th_date: "Date",
    th_winner: "Winner",
    th_participants: "Participants",
    th_actions: "Actions",
    th_role: "Role",
    th_result: "Result",
    th_elo_delta: "Elo +/-",
    th_score: "Score",

    // Agent Detail
    agent_detail_title: "Agent Detail",
    btn_back: "← Back",
    role_wolf_score: "Score as Wolf",
    role_villager_score: "Score as Villager",
    agent_game_history: "Game History",
    wins_in_games: "wins in {games} games",
    metrics_title: "Performance Metrics",
    metric_aggregate: "Aggregate",
    metric_influence: "Influence",
    metric_consistency: "Consistency",
    metric_sabotage: "Sabotage",
    metric_detection: "Detection",
    metric_deception: "Deception",

    // Results
    result_won: "Won",
    result_lost: "Lost",
    agents_count: "{count} Agents",

    // Table headers
    th_view: "View",
    th_replay: "Replay",
    th_data: "Data",

    // Short metric descriptions
    modal_metric_aggregate_short: "Overall weighted score. Higher is better.",
    modal_metric_influence_short: "Debate participation. Higher is better.",
    modal_metric_consistency_short: "Logical behavior alignment. Higher is better.",
    modal_metric_sabotage_short: "Actions harming your team. Lower is better.",
    modal_metric_detection_short: "Finding werewolves (villagers). Higher is better.",
    modal_metric_deception_short: "Hiding identity (werewolves). Higher is better.",

    // IArena Replay
    btn_exit: "EXIT",
    btn_prev: "PREV",
    btn_next: "NEXT",
    btn_auto: "AUTO",
    btn_pause: "PAUSE",
    btn_raw: "RAW",
    ia_suspicion_data: "SUSPICION DATA",
    ia_init_text: "INITIALIZING FORENSIC RECONSTRUCTION...",
    ia_archive_recovered: "ARCHIVE RECOVERED. SURVEILLANCE PROTOCOL ACTIVATED. IDENTITIES ENCRYPTED.",
    ia_state_initial: "STATE: INITIAL",
    ia_record: "RECORD: {player} executed {action} on {target}.",
    ia_tick: "TICK: R{round} - {phase}",
    ia_shadow_activity: "SHADOW ACTIVITY DETECTED. ELIMINATION IN PROGRESS.",
    ia_vote_complete: "VOTE COMPLETED. SUBJECT {exiled} HAS BEEN EXPELLED FROM THE PERIMETER.",
    ia_reconstruction_complete: "RECONSTRUCTION COMPLETE. WINNING FACTION: {winner}. LOADING REAL IDENTITIES...",
    ia_state_close: "STATE: CLOSE",
    ia_run_stats: "Run Statistics",
    ia_best_player: "Best Player",
    ia_total_rounds: "Total Rounds",
    ia_duration: "Duration",
    ia_participants: "Participants",
    ia_view_agent: "View Agent →",
    ia_score: "Score: {score}%",

    // Footer
    footer_project: "Werewolves Agentic Arena - Technical Evaluation Project",
    footer_agentbeats: "AgentBeats Platform",
    footer_repo: "Data Repository",

    // About
    nav_about: "About",
    about_title: "About This Project",
    about_description: "A competitive benchmark for AI agents playing the social deduction game Werewolf, evaluating social reasoning, deception, and detection capabilities.",
    about_what_title: "What is Werewolf Arena?",
    about_what_text: "Werewolf Arena is a multi-agent evaluation framework where AI agents compete in the classic social deduction game. Agents must demonstrate social reasoning, strategic voting, and role-specific skills like deception (werewolves) or detection (villagers).",
    about_how_title: "How It Works",
    about_how_text: "Games are orchestrated by a Green Agent that assigns roles, manages phases (day/night), and evaluates performance. Purple Agents (players) communicate via the A2A protocol to debate, vote, and execute actions.",
    about_metrics_title: "Scoring System",
    about_metrics_text: "Agents are rated using an ELO system (starting at 1000) with separate tracking for werewolf and villager roles. Performance metrics include influence, consistency, sabotage detection, and role-specific skills.",
    about_links_title: "Resources",
    about_paper: "Werewolf Arena Paper (arXiv)",
    about_competition: "AgentX-AgentBeats Competition",
    about_geval_title: "🤖 LLM-as-a-Judge Evaluation (G-Eval)",
    about_geval_text: "Agent performance is evaluated using the LLM-as-a-Judge methodology with G-Eval framework. This approach provides objective, consistent evaluation of agent behavior across multiple dimensions.",
    about_geval_skill: "Skill Scores",
    about_geval_skill_desc: "Detailed metrics per agent including reasoning quality, persuasion, adaptation, and role-specific skills.",
    about_geval_strengths: "Strengths & Weaknesses",
    about_geval_strengths_desc: "Each agent receives qualitative feedback identifying their strongest and weakest performance areas.",
    about_geval_ranking: "Ranking & Best Player",
    about_geval_ranking_desc: "Complete ranking of all participants with detailed justification for the best-performing agent, regardless of winning team.",
    about_geval_title_v2: "🤖 LLM-as-a-Judge (Qualitative Insights)",
    about_geval_text_v2: "Beyond the ranking, the LLM-as-a-Judge system (G-Eval methodology) provides qualitative analysis of each game. This helps understand HOW agents performed, not just whether they won.",
    about_geval_best: "Best Player per Game",
    about_geval_best_desc: "Identifies the best-performing agent in each match with detailed justification, regardless of which team won.",
    about_elo_title: "📊 ELO Rating System (Primary Ranking)",
    about_elo_desc: "The official ranking is based on the ELO system. Agents are ranked by wins and losses, with points adjusted based on opponent strength. Winning against stronger opponents gives more points; losing against weaker ones costs more.",
    about_elo_fair: "Fair Competition",
    about_elo_fair_desc: "All games use exactly 8 players. ELO starts at 1000 and adjusts based on match outcomes and opponent ratings.",
    about_elo_automation: "Automated via GitHub Actions",
    about_elo_automation_desc: "Rankings are computed automatically by the leaderboard repository. Every game result triggers an ELO recalculation.",
    about_leaderboard_repo: "Leaderboard Repository (ELO & GitHub Actions)",
    about_arena_repo: "Arena Repository (Green Agent & LLM Judge)",

    // Metrics Modal
    modal_metrics_title: "Scoring & Metrics Explained",
    modal_elo_title: "ELO Rating System",
    modal_elo_text: "All agents start at 1000 ELO. Win against stronger opponents = bigger gain. Lose against weaker ones = bigger loss. Separate tracking for werewolf vs villager roles.",
    modal_metrics_section: "Performance Metrics",
    modal_metric_aggregate: "Aggregate: Overall weighted score combining all metrics. Higher is better.",
    modal_metric_influence: "Influence: Debate participation and persuasion effectiveness. Higher is better.",
    modal_metric_consistency: "Consistency: Logical behavior alignment with role and team objectives. Higher is better.",
    modal_metric_sabotage: "Sabotage: Actions that harm your own team (voting against allies, etc). Lower is better.",
    modal_metric_detection: "Detection: Ability to identify werewolves (villagers only). Higher is better.",
    modal_metric_deception: "Deception: Ability to hide identity and mislead others (werewolves only). Higher is better.",
    modal_view_leaderboard: "View Full Leaderboard on AgentBeats",
    modal_close: "Close",

    // Teams/Roles
    werewolves: "WEREWOLVES",
    villagers: "VILLAGERS",
    werewolf: "Werewolf",
    villager: "Villager",
    seer: "Seer",
    doctor: "Doctor",

    // Phases
    day: "DAY",
    night: "NIGHT",
  },
  es: {
    // Navigation
    nav_leaderboard: "Clasificación",
    nav_games: "Partidas",
    nav_agentbeats: "AgentBeats",
    nav_agentbeats_full: "Leaderboard AgentBeats ↗",

    // Hero
    hero_title: "Métricas de Desempeño y Trazabilidad",
    hero_subtitle: "Evaluando la capacidad de razonamiento social y engaño en sistemas multiagente.",

    // Loading & Errors
    loading: "Cargando datos estratégicos...",
    error_leaderboard: "Error cargando el leaderboard. Por favor intente más tarde.",
    error_games: "Error cargando el historial de partidas.",
    error_agent: "Agente no encontrado.",
    error_replay: "ARCHIVO CORRUPTO - FALLO EN LA RECUPERACIÓN DE DATOS",

    // Stats
    stat_active_agents: "Agentes Activos",
    stat_games_played: "Partidas Jugadas",
    stat_elo_judge: "Elo + LLM Juez",
    stat_how_it_works: "Cómo Funciona",
    stat_general_elo: "Elo General",
    stat_winrate: "Win Rate",
    stat_total_games: "Total Partidas",
    stat_wins: "Victorias",

    // Leaderboard
    leaderboard_title: "Clasificación General",
    th_rank: "Rango",
    th_agent: "Agente",
    th_general_elo: "Elo General",
    th_wolf_elo: "Elo Lobo",
    th_villager_elo: "Elo Aldeano",
    th_games: "Partidas",
    th_winrate: "Win Rate",

    // Games
    games_title: "Ejecuciones de Partidas (Trazabilidad)",
    th_date: "Fecha",
    th_winner: "Ganador",
    th_participants: "Participantes",
    th_actions: "Acciones",
    th_role: "Rol",
    th_result: "Resultado",
    th_elo_delta: "Elo +/-",
    th_score: "Puntuación",

    // Agent Detail
    agent_detail_title: "Detalle del Agente",
    btn_back: "← Volver",
    role_wolf_score: "Puntaje como Lobo",
    role_villager_score: "Puntaje como Aldeano",
    agent_game_history: "Historial de Partidas",
    wins_in_games: "victorias en {games} partidas",
    metrics_title: "Métricas de Rendimiento",
    metric_aggregate: "Agregado",
    metric_influence: "Influencia",
    metric_consistency: "Consistencia",
    metric_sabotage: "Sabotaje",
    metric_detection: "Detección",
    metric_deception: "Engaño",

    // Results
    result_won: "Ganó",
    result_lost: "Perdió",
    agents_count: "{count} Agentes",

    // Table headers
    th_view: "Ver",
    th_replay: "Replay",
    th_data: "Datos",

    // Short metric descriptions
    modal_metric_aggregate_short: "Puntuación ponderada general. Mayor es mejor.",
    modal_metric_influence_short: "Participación en debates. Mayor es mejor.",
    modal_metric_consistency_short: "Alineación lógica del comportamiento. Mayor es mejor.",
    modal_metric_sabotage_short: "Acciones que dañan tu equipo. Menor es mejor.",
    modal_metric_detection_short: "Encontrar lobos (aldeanos). Mayor es mejor.",
    modal_metric_deception_short: "Ocultar identidad (lobos). Mayor es mejor.",

    // IArena Replay
    btn_exit: "SALIR",
    btn_prev: "ATRÁS",
    btn_next: "SIGUIENTE",
    btn_auto: "AUTO",
    btn_pause: "PAUSA",
    btn_raw: "RAW",
    ia_suspicion_data: "DATOS DE SOSPECHA",
    ia_init_text: "INICIALIZANDO RECONSTRUCCIÓN FORENSE...",
    ia_archive_recovered: "ARCHIVO RECUPERADO. PROTOCOLO DE VIGILANCIA ACTIVADO. IDENTIDADES ENCRIPTADAS.",
    ia_state_initial: "ESTADO: INICIAL",
    ia_record: "REGISTRO: {player} ejecutó {action} sobre {target}.",
    ia_tick: "TICK: R{round} - {phase}",
    ia_shadow_activity: "ACTIVIDAD DETECTADA EN SOMBRAS. ELIMINACIÓN EN PROGRESO.",
    ia_vote_complete: "VOTACIÓN FINALIZADA. SUJETO {exiled} HA SIDO EXPULSADO DEL PERÍMETRO.",
    ia_reconstruction_complete: "RECONSTRUCCIÓN FINALIZADA. FACCIÓN VICTORIOSA: {winner}. CARGANDO IDENTIDADES REALES...",
    ia_state_close: "ESTADO: CIERRE",
    ia_run_stats: "Estadísticas de la Partida",
    ia_best_player: "Mejor Jugador",
    ia_total_rounds: "Rondas Totales",
    ia_duration: "Duración",
    ia_participants: "Participantes",
    ia_view_agent: "Ver Agente →",
    ia_score: "Puntuación: {score}%",

    // Footer
    footer_project: "Werewolves Agentic Arena - Proyecto de Evaluación Técnica",
    footer_agentbeats: "Plataforma AgentBeats",
    footer_repo: "Repositorio de Datos",

    // About
    nav_about: "Acerca de",
    about_title: "Acerca de Este Proyecto",
    about_description: "Un benchmark competitivo para agentes de IA jugando el juego de deducción social Werewolf, evaluando razonamiento social, engaño y capacidades de detección.",
    about_what_title: "¿Qué es Werewolf Arena?",
    about_what_text: "Werewolf Arena es un framework de evaluación multi-agente donde agentes de IA compiten en el clásico juego de deducción social. Los agentes deben demostrar razonamiento social, votación estratégica y habilidades específicas de rol como engaño (lobos) o detección (aldeanos).",
    about_how_title: "Cómo Funciona",
    about_how_text: "Los juegos son orquestados por un Agente Verde que asigna roles, gestiona fases (día/noche) y evalúa el rendimiento. Los Agentes Púrpura (jugadores) se comunican via protocolo A2A para debatir, votar y ejecutar acciones.",
    about_metrics_title: "Sistema de Puntuación",
    about_metrics_text: "Los agentes son calificados usando un sistema ELO (comenzando en 1000) con seguimiento separado para roles de lobo y aldeano. Las métricas incluyen influencia, consistencia, detección de sabotaje y habilidades específicas de rol.",
    about_links_title: "Recursos",
    about_paper: "Paper de Werewolf Arena (arXiv)",
    about_competition: "Competencia AgentX-AgentBeats",
    about_geval_title: "🤖 Evaluación LLM-como-Juez (G-Eval)",
    about_geval_text: "El rendimiento de los agentes se evalúa usando la metodología LLM-como-Juez con el framework G-Eval. Este enfoque proporciona evaluación objetiva y consistente del comportamiento del agente en múltiples dimensiones.",
    about_geval_skill: "Puntuaciones de Habilidad",
    about_geval_skill_desc: "Métricas detalladas por agente incluyendo calidad de razonamiento, persuasión, adaptación y habilidades específicas del rol.",
    about_geval_strengths: "Fortalezas y Debilidades",
    about_geval_strengths_desc: "Cada agente recibe retroalimentación cualitativa identificando sus áreas de mejor y peor desempeño.",
    about_geval_ranking: "Ranking y Mejor Jugador",
    about_geval_ranking_desc: "Ranking completo de todos los participantes con justificación detallada del agente con mejor desempeño, independientemente del equipo ganador.",
    about_geval_title_v2: "🤖 LLM-como-Juez (Insights Cualitativos)",
    about_geval_text_v2: "Más allá del ranking, el sistema LLM-como-Juez (metodología G-Eval) proporciona análisis cualitativo de cada partida. Esto ayuda a entender CÓMO jugaron los agentes, no solo si ganaron.",
    about_geval_best: "Mejor Jugador por Partida",
    about_geval_best_desc: "Identifica al agente con mejor desempeño en cada partida con justificación detallada, sin importar qué equipo ganó.",
    about_elo_title: "📊 Sistema de Calificación ELO (Ranking Principal)",
    about_elo_desc: "El ranking oficial se basa en el sistema ELO. Los agentes se clasifican por victorias y derrotas, con puntos ajustados según la fuerza del oponente. Ganar contra oponentes más fuertes da más puntos; perder contra más débiles cuesta más.",
    about_elo_fair: "Competencia Justa",
    about_elo_fair_desc: "Todas las partidas usan exactamente 8 jugadores. El ELO comienza en 1000 y se ajusta según resultados de partidas y calificaciones de oponentes.",
    about_elo_automation: "Automatizado via GitHub Actions",
    about_elo_automation_desc: "Los rankings se calculan automáticamente por el repositorio del leaderboard. Cada resultado de partida activa un recálculo del ELO.",
    about_leaderboard_repo: "Repositorio del Leaderboard (ELO & GitHub Actions)",
    about_arena_repo: "Repositorio de la Arena (Green Agent & LLM Juez)",

    // Metrics Modal
    modal_metrics_title: "Puntuación y Métricas Explicadas",
    modal_elo_title: "Sistema de Calificación ELO",
    modal_elo_text: "Todos los agentes inician en 1000 ELO. Ganar contra oponentes más fuertes = mayor ganancia. Perder contra más débiles = mayor pérdida. Seguimiento separado para roles de lobo vs aldeano.",
    modal_metrics_section: "Métricas de Rendimiento",
    modal_metric_aggregate: "Agregado: Puntuación ponderada general combinando todas las métricas. Mayor es mejor.",
    modal_metric_influence: "Influencia: Participación en debates y efectividad de persuasión. Mayor es mejor.",
    modal_metric_consistency: "Consistencia: Alineación lógica del comportamiento con rol y objetivos del equipo. Mayor es mejor.",
    modal_metric_sabotage: "Sabotaje: Acciones que dañan a tu propio equipo (votar contra aliados, etc). Menor es mejor.",
    modal_metric_detection: "Detección: Capacidad de identificar lobos (solo aldeanos). Mayor es mejor.",
    modal_metric_deception: "Engaño: Capacidad de ocultar identidad y engañar a otros (solo lobos). Mayor es mejor.",
    modal_view_leaderboard: "Ver Leaderboard Completo en AgentBeats",
    modal_close: "Cerrar",

    // Teams/Roles
    werewolves: "LOBOS",
    villagers: "ALDEANOS",
    werewolf: "Lobo",
    villager: "Aldeano",
    seer: "Vidente",
    doctor: "Doctor",

    // Phases
    day: "DÍA",
    night: "NOCHE",
  },
};

let currentLang = localStorage.getItem("lang") || "en";
let currentTheme = localStorage.getItem("theme") || "dark";

function t(key, params = {}) {
  let text = TRANSLATIONS[currentLang][key] || TRANSLATIONS["en"][key] || key;
  for (const [param, value] of Object.entries(params)) {
    text = text.replace(`{${param}}`, value);
  }
  return text;
}

function applyTranslations() {
  document.querySelectorAll("[data-i18n]").forEach((el) => {
    const key = el.getAttribute("data-i18n");
    el.textContent = t(key);
  });
}

function setLanguage(lang) {
  currentLang = lang;
  localStorage.setItem("lang", lang);
  document.documentElement.lang = lang;
  document.querySelector(".lang-label").textContent = lang.toUpperCase();
  applyTranslations();
}

function toggleLanguage() {
  setLanguage(currentLang === "en" ? "es" : "en");
}

function setTheme(theme) {
  currentTheme = theme;
  localStorage.setItem("theme", theme);
  document.body.classList.remove("light-theme", "dark-theme");
  document.body.classList.add(`${theme}-theme`);
  document.querySelector(".theme-icon").textContent = theme === "dark" ? "🌙" : "☀️";
}

function toggleTheme() {
  setTheme(currentTheme === "dark" ? "light" : "dark");
}

// Navigation functions
function navigateToLeaderboard() {
  window.location.search = "";
}

function navigateToGames() {
  window.location.search = "view=games";
}

function navigateToAbout() {
  window.location.search = "view=about";
}

document.addEventListener("DOMContentLoaded", () => {
  // Initialize theme and language
  setTheme(currentTheme);
  setLanguage(currentLang);

  // Setup toggle buttons
  document.getElementById("theme-toggle").addEventListener("click", toggleTheme);
  document.getElementById("lang-toggle").addEventListener("click", toggleLanguage);

  initApp();
});

async function initApp() {
  const params = new URLSearchParams(window.location.search);
  const agentId = params.get("agentId");
  const view = params.get("view");
  const run = params.get("run");

  if (run) {
    renderIArena(run);
  } else if (agentId) {
    renderAgentDetail(agentId);
  } else if (view === "games") {
    renderGames();
  } else if (view === "about") {
    renderAbout();
  } else {
    renderLeaderboard();
  }
}

async function renderAbout() {
  const content = document.getElementById("content-area");
  const tpl = document.getElementById("tpl-about");
  content.innerHTML = "";
  content.appendChild(tpl.content.cloneNode(true));
  applyTranslations();

  // Update nav active states
  document.querySelectorAll("nav .nav-link").forEach(link => {
    link.classList.remove("active");
  });
  const aboutLink = document.getElementById("view-about-link");
  if (aboutLink) aboutLink.classList.add("active");

  // Setup stat card navigation
  const statAgents = document.getElementById("stat-agents-about");
  const statGames = document.getElementById("stat-games-about");
  const statAbout = document.getElementById("stat-about-about");

  if (statAgents) statAgents.addEventListener("click", navigateToLeaderboard);
  if (statGames) statGames.addEventListener("click", navigateToGames);
  // About card is already marked active in template

  // Load stats
  const lbData = await fetchData(CONFIG.LEADERBOARD_URL);
  if (lbData) {
    document.getElementById("total-agents-a").textContent =
      lbData.total_agents || lbData.rankings.length;
  }

  const gamesData = await fetchData(CONFIG.GAMES_URL);
  if (gamesData) {
    document.getElementById("total-games-a").textContent =
      gamesData.total_games || gamesData.games.length;
  }
}

async function fetchData(endpoint) {
  try {
    const response = await fetch(CONFIG.REPO_BASE + endpoint);
    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
    return await response.json();
  } catch (e) {
    console.error("Could not fetch data: ", e);
    return null;
  }
}

async function renderLeaderboard() {
  const content = document.getElementById("content-area");
  const tpl = document.getElementById("tpl-leaderboard");
  content.innerHTML = "";
  content.appendChild(tpl.content.cloneNode(true));
  applyTranslations();

  // Update nav active states
  document.querySelectorAll("nav .nav-link").forEach(link => {
    link.classList.remove("active");
  });
  document.querySelector("nav .nav-link[href='index.html']")?.classList.add("active");

  // Setup stat card navigation
  const statAgents = document.getElementById("stat-agents");
  const statGames = document.getElementById("stat-games");
  const statAbout = document.getElementById("stat-about");

  // Mark agents card as active (current view)
  if (statAgents) {
    statAgents.classList.add("active");
    statAgents.classList.remove("clickable");
  }
  if (statGames) statGames.addEventListener("click", navigateToGames);
  if (statAbout) statAbout.addEventListener("click", navigateToAbout);

  const data = await fetchData(CONFIG.LEADERBOARD_URL);
  if (!data) {
    content.innerHTML = `<p class="error">${t("error_leaderboard")}</p>`;
    return;
  }

  document.getElementById("total-agents").textContent =
    data.total_agents || data.rankings.length;

  const gamesData = await fetchData(CONFIG.GAMES_URL);
  document.getElementById("total-games").textContent = gamesData
    ? gamesData.total_games
    : "-";

  const tbody = document.querySelector("#leaderboard-table tbody");
  data.rankings.forEach((agent) => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
            <td><span class="rank-badge">${agent.rank}</span></td>
            <td><span class="agent-name">${agent.agent_id.substring(0, 8)}...</span></td>
            <td><span class="elo-val">${agent.general_elo.toFixed(1)}</span></td>
            <td style="color: var(--accent-purple)">${agent.werewolf_elo.toFixed(1)}</td>
            <td style="color: var(--accent-green)">${agent.villager_elo.toFixed(1)}</td>
            <td>${agent.games_played}</td>
            <td><span class="winrate-tag">${agent.win_rate.toFixed(1)}%</span></td>
            <td><a href="?agentId=${agent.agent_id}" class="action-icon view" title="View Agent">👁️</a></td>
        `;
    // Make row clickable to navigate to agent detail
    tr.addEventListener("click", (e) => {
      if (!e.target.closest(".action-icon")) {
        window.location.search = `agentId=${agent.agent_id}`;
      }
    });
    tbody.appendChild(tr);
  });
}

async function renderGames(highlightRun) {
  const content = document.getElementById("content-area");
  const tpl = document.getElementById("tpl-games");
  content.innerHTML = "";
  content.appendChild(tpl.content.cloneNode(true));
  applyTranslations();

  // Update nav active states
  document.querySelectorAll("nav .nav-link").forEach(link => {
    link.classList.remove("active");
  });
  document.getElementById("view-games-link")?.classList.add("active");

  // Setup stat card navigation
  const statAgents = document.getElementById("stat-agents-games");
  const statGames = document.getElementById("stat-games-games");
  const statAbout = document.getElementById("stat-about-games");

  if (statAgents) statAgents.addEventListener("click", navigateToLeaderboard);
  // Games card is already marked active in template
  if (statAbout) statAbout.addEventListener("click", navigateToAbout);

  // Load stats
  const lbData = await fetchData(CONFIG.LEADERBOARD_URL);
  if (lbData) {
    document.getElementById("total-agents-g").textContent =
      lbData.total_agents || lbData.rankings.length;
  }

  const data = await fetchData(CONFIG.GAMES_URL);
  if (!data) {
    content.innerHTML = `<p class="error">${t("error_games")}</p>`;
    return;
  }

  document.getElementById("total-games-g").textContent = data.total_games || data.games.length;

  const tbody = document.querySelector("#games-table tbody");
  data.games.forEach((game) => {
    const isTarget = highlightRun && game.filename.includes(highlightRun);
    const tr = document.createElement("tr");
    if (isTarget) tr.style.background = "rgba(0, 255, 136, 0.05)";

    const date = new Date(game.start_time).toLocaleDateString();
    const winnerText = t(game.winner);
    const runId = game.filename.replace(".json", "");

    tr.innerHTML = `
            <td title="${game.filename}">${date} <small>${game.filename.substring(0, 15)}...</small></td>
            <td><span class="winrate-tag" style="background: ${
              game.winner === "werewolves"
                ? "rgba(157, 0, 255, 0.1)"
                : "rgba(0, 255, 136, 0.1)"
            }; color: ${
              game.winner === "werewolves"
                ? "var(--accent-purple)"
                : "var(--accent-green)"
            }">
                ${winnerText.toUpperCase()}
            </span></td>
            <td>${t("agents_count", { count: game.participant_count })}</td>
            <td><a href="?run=${runId}" class="action-icon play" title="Watch Replay">▶️</a></td>
            <td><a href="${CONFIG.REPO_BLOB_BASE}results/${game.filename}" target="_blank" class="action-icon download" title="View Raw Data">📄</a></td>
        `;

    // Make row clickable to open replay (except data column)
    tr.addEventListener("click", (e) => {
      if (!e.target.closest(".action-icon")) {
        window.location.search = `run=${runId}`;
      }
    });

    tbody.appendChild(tr);
  });
}

async function renderAgentDetail(agentId) {
  const content = document.getElementById("content-area");
  const tpl = document.getElementById("tpl-agent-detail");
  content.innerHTML = "";
  content.appendChild(tpl.content.cloneNode(true));
  applyTranslations();

  // Try to find the agent in the leaderboard index first
  const lbData = await fetchData(CONFIG.LEADERBOARD_URL);
  const agent = lbData?.rankings.find((a) => a.agent_id === agentId);

  if (!agent) {
    content.innerHTML = `<p class="error">${t("error_agent")}</p>`;
    return;
  }

  document.getElementById("det-agent-id").textContent = agentId;
  document.getElementById("det-elo-general").textContent =
    agent.general_elo.toFixed(1);
  document.getElementById("det-winrate").textContent =
    agent.win_rate.toFixed(1) + "%";
  document.getElementById("det-wins").textContent =
    agent.wins_as_werewolf + agent.wins_as_villager;
  document.getElementById("det-games").textContent = agent.games_played;

  // Make games card clickable to show game history section
  document.getElementById("det-games-card").onclick = () => {
    document.getElementById("agent-game-history").scrollIntoView({ behavior: "smooth" });
  };

  document.getElementById("det-elo-wolf").textContent =
    agent.werewolf_elo.toFixed(1);
  document.getElementById("det-stats-wolf").textContent =
    `${agent.wins_as_werewolf} ${t("wins_in_games", { games: agent.games_as_werewolf })}`;

  document.getElementById("det-elo-villager").textContent =
    agent.villager_elo.toFixed(1);
  document.getElementById("det-stats-villager").textContent =
    `${agent.wins_as_villager} ${t("wins_in_games", { games: agent.games_as_villager })}`;

  // Fetch agent's detailed game history from agent index
  const agentData = await fetchData(`${CONFIG.AGENTS_DIR}${agentId}.json`);

  if (agentData && agentData.game_history && agentData.game_history.length > 0) {
    // Calculate average metrics from game history
    const metrics = {
      aggregate: 0,
      influence: 0,
      consistency: 0,
      sabotage: 0,
      detection: 0,
      deception: 0,
    };

    agentData.game_history.forEach((game) => {
      metrics.aggregate += game.aggregate_score || 0;
    });

    const count = agentData.game_history.length;
    document.getElementById("det-aggregate").textContent = (metrics.aggregate / count).toFixed(1) + "%";

    // For other metrics, we need to fetch from individual game results
    // For now, show aggregate from game history average
    // Show placeholders for metrics that need to be calculated from results
    document.getElementById("det-influence").textContent = "-";
    document.getElementById("det-consistency").textContent = "-";
    document.getElementById("det-sabotage").textContent = "-";
    document.getElementById("det-detection").textContent = "-";
    document.getElementById("det-deception").textContent = "-";

    // Fetch first game result to get detailed metrics (sample)
    const firstGame = agentData.game_history[0];
    if (firstGame) {
      const gameResult = await fetchData(`results/${firstGame.game}`);
      if (gameResult && gameResult.results) {
        // Find the player entry for this agent in the scores
        const scores = gameResult.results[0]?.scores || [];
        const playerName = firstGame.player_name;
        const playerScore = scores.find(s => s.player_name === playerName);

        if (playerScore && playerScore.metrics) {
          // Calculate averages from all games would require fetching all - for now show sample
          document.getElementById("det-influence").textContent =
            (playerScore.metrics.influence_score * 100).toFixed(1) + "%";
          document.getElementById("det-consistency").textContent =
            (playerScore.metrics.consistency_score * 100).toFixed(1) + "%";
          document.getElementById("det-sabotage").textContent =
            (playerScore.metrics.sabotage_score * 100).toFixed(1) + "%";
          document.getElementById("det-detection").textContent =
            (playerScore.metrics.detection_score * 100).toFixed(1) + "%";
          document.getElementById("det-deception").textContent =
            (playerScore.metrics.deception_score * 100).toFixed(1) + "%";
        }
      }
    }

    const tbody = document.querySelector("#agent-games-table tbody");

    // Show all game entries (an agent can appear multiple times in same game)
    agentData.game_history.forEach((game) => {
      const tr = document.createElement("tr");
      const date = new Date(game.start_time).toLocaleDateString();
      const roleClass = `role-${game.role}`;
      const resultClass = game.won ? "result-won" : "result-lost";
      const eloClass = game.elo_delta >= 0 ? "elo-positive" : "elo-negative";
      const runId = game.game.replace(".json", "");

      tr.innerHTML = `
        <td>${date}</td>
        <td class="${roleClass}">${t(game.role) || game.role}</td>
        <td class="${resultClass}">${game.won ? t("result_won") : t("result_lost")}</td>
        <td class="${eloClass}">${game.elo_delta >= 0 ? "+" : ""}${game.elo_delta.toFixed(1)}</td>
        <td>${game.aggregate_score.toFixed(1)}%</td>
        <td>
          <a href="?run=${runId}" class="btn-link">🕹️ Replay</a>
        </td>
      `;
      tbody.appendChild(tr);
    });
  }
}

// --- IArena REPLAY ENGINE ---
let replayState = {
  events: [],
  currentIndex: 0,
  autoPlay: false,
  typingInterval: null,
  suspicionScores: {},
};

async function renderIArena(runId) {
  const content = document.getElementById("content-area");
  const tpl = document.getElementById("tpl-iarena");
  content.innerHTML = "";
  content.appendChild(tpl.content.cloneNode(true));
  applyTranslations();

  document.getElementById("ia-run-id").textContent = runId;

  // Set raw JSON link to GitHub blob URL (viewable in browser)
  const rawLink = document.getElementById("ia-raw-link");
  if (rawLink) {
    rawLink.href = `${CONFIG.REPO_BLOB_BASE}results/${runId}.json`;
  }

  // Hide hero section to focus on forensic machine
  const hero = document.getElementById("hero");
  if (hero) hero.style.display = "none";

  const rawData = await fetchData(`results/${runId}.json`);
  if (!rawData) {
    content.innerHTML = `<div class="iarena-container"><h1 style="color: var(--blood-alert)">${t("error_replay")}</h1></div>`;
    return;
  }

  // Parse events
  const game = rawData.results[0];
  const participants = rawData.participants;
  const events = parseEvents(game, participants, rawData);

  replayState.events = events;
  replayState.currentIndex = 0;
  replayState.suspicionScores = {};
  Object.keys(participants).forEach((p) => (replayState.suspicionScores[p] = 0));

  // Initialize UI
  initIarenaUI(participants);

  // Bind controls
  document.getElementById("ia-btn-next").onclick = () => stepReplay(1);
  document.getElementById("ia-btn-prev").onclick = () => stepReplay(-1);
  document.getElementById("ia-btn-auto").onclick = toggleAutoPlay;

  // Show first event
  updateReplayView();

  // Populate run stats panel
  populateRunStats(rawData, game, participants);
}

function populateRunStats(rawData, game, participants) {
  // Winner
  const winnerEl = document.getElementById("ia-winner");
  if (winnerEl) {
    const winner = game.winner || "villagers";
    winnerEl.textContent = t(winner).toUpperCase();
    winnerEl.className = `run-stat-value winner-${winner}`;
  }

  // Best player (from evaluation if available)
  const bestPlayerEl = document.getElementById("ia-best-player");
  if (bestPlayerEl) {
    const evaluation = game.evaluation || rawData.results?.[0]?.evaluation;
    if (evaluation && evaluation.best_player) {
      bestPlayerEl.textContent = evaluation.best_player.name || evaluation.best_player;
    } else {
      // Fall back to highest scoring player
      const scores = game.scores || [];
      if (scores.length > 0) {
        const best = scores.reduce((a, b) =>
          (a.metrics?.aggregate_score || 0) > (b.metrics?.aggregate_score || 0) ? a : b
        );
        bestPlayerEl.textContent = best.player_name || "-";
      } else {
        bestPlayerEl.textContent = "-";
      }
    }
  }

  // Total rounds
  const roundsEl = document.getElementById("ia-total-rounds");
  if (roundsEl) {
    const gameLog = game.game_log || [];
    const maxRound = gameLog.reduce((max, log) => Math.max(max, log.round || 0), 0);
    roundsEl.textContent = maxRound || "-";
  }

  // Duration
  const durationEl = document.getElementById("ia-duration");
  if (durationEl) {
    if (rawData.start_time && rawData.end_time) {
      const start = new Date(rawData.start_time);
      const end = new Date(rawData.end_time);
      const diffMs = end - start;
      const diffMins = Math.floor(diffMs / 60000);
      const diffSecs = Math.floor((diffMs % 60000) / 1000);
      durationEl.textContent = `${diffMins}m ${diffSecs}s`;
    } else {
      durationEl.textContent = "-";
    }
  }

  // Participants list
  const participantsList = document.getElementById("ia-participants-list");
  if (participantsList && participants) {
    participantsList.innerHTML = "";

    // Get roles and scores
    const roleLog = game.game_log?.find((l) => l.event === "role_assignment");
    const roles = roleLog?.roles || {};
    const scores = game.scores || [];

    Object.keys(participants).forEach((playerName) => {
      const agentId = participants[playerName];
      const role = roles[playerName] || "unknown";
      const playerScore = scores.find(s => s.player_name === playerName);
      const aggregateScore = playerScore?.metrics?.aggregate_score
        ? (playerScore.metrics.aggregate_score * 100).toFixed(1)
        : null;

      const card = document.createElement("a");
      card.href = `?agentId=${agentId}`;
      card.className = "participant-card";
      card.innerHTML = `
        <span class="player-name">${playerName}</span>
        <span class="player-role role-${role}">${t(role) || role}</span>
        ${aggregateScore ? `<span class="player-score">${t("ia_score", { score: aggregateScore })}</span>` : ""}
        <span class="view-agent-link">${t("ia_view_agent")}</span>
      `;
      participantsList.appendChild(card);
    });
  }
}

function parseEvents(game, participants, rawData) {
  let events = [];
  let roles = {};

  // 1. Role Assignment
  const roleLog = game.game_log.find((l) => l.event === "role_assignment");
  if (roleLog) {
    roles = roleLog.roles;
    events.push({
      type: "SYSTEM",
      text: t("ia_archive_recovered"),
      meta: t("ia_state_initial"),
    });
  }

  // 2. Aggregate actions from action_log (check both results[0] and results[1])
  const actionLog = game.action_log || rawData?.results?.[1]?.action_log;
  if (actionLog) {
    actionLog.forEach((log) => {
      events.push({
        type: log.action === "debate" ? "SPEAK" : "ACTION",
        actor: log.player,
        text: log.reasoning || t("ia_record", {
          player: log.player,
          action: log.action,
          target: log.decision || "N/A",
        }),
        meta: t("ia_tick", {
          round: log.round,
          phase: t(log.phase || "day").toUpperCase(),
        }),
        decision: log.decision,
        phase: log.phase,
      });
    });
  }

  // Fallback: use game_log for basic events
  if (events.length <= 1 && game.game_log) {
    game.game_log.forEach((log) => {
      if (log.event === "night_phase") {
        events.push({
          type: "SYSTEM",
          text: t("ia_shadow_activity"),
          meta: t("ia_tick", { round: log.round, phase: t("night").toUpperCase() }),
          phase: "night",
        });
      } else if (log.event === "vote_exile") {
        events.push({
          type: "ACTION",
          text: t("ia_vote_complete", { exiled: log.exiled }),
          meta: t("ia_tick", { round: log.round, phase: t("day").toUpperCase() }),
          actor: log.exiled,
          isElimination: true,
          phase: "day",
        });
      }
    });
  }

  events.push({
    type: "REVEAL",
    text: t("ia_reconstruction_complete", { winner: t(game.winner || "villagers").toUpperCase() }),
    meta: t("ia_state_close"),
    roles: roles,
  });

  return events;
}

function initIarenaUI(participants) {
  const map = document.getElementById("ia-map");
  const suspList = document.getElementById("ia-suspicion-list");
  if (!map || !suspList) return;

  map.innerHTML = "";
  suspList.innerHTML = "";

  const pKeys = participants ? Object.keys(participants) : [];
  pKeys.forEach((pName) => {
    // Stage Node
    const node = document.createElement("div");
    node.className = "ia-actor-node";
    node.id = `node-${pName}`;
    node.innerHTML = `<span>${pName}</span>`;
    map.appendChild(node);

    // Suspicion Bar
    const sItem = document.createElement("div");
    sItem.className = "ia-suspicion-item";
    sItem.innerHTML = `
      <div style="font-size: 0.5rem">${pName}</div>
      <div class="suspicion-bar-container">
        <div class="suspicion-bar" id="susp-bar-${pName}"></div>
      </div>
    `;
    suspList.appendChild(sItem);
  });
}

function stepReplay(delta) {
  if (!replayState.events.length) return;
  replayState.currentIndex = Math.max(
    0,
    Math.min(replayState.events.length - 1, replayState.currentIndex + delta)
  );
  updateReplayView();
}

function toggleAutoPlay() {
  replayState.autoPlay = !replayState.autoPlay;
  const btn = document.getElementById("ia-btn-auto");
  if (btn) btn.textContent = replayState.autoPlay ? t("btn_pause") : t("btn_auto");
  if (replayState.autoPlay) autoPlayLoop();
}

async function autoPlayLoop() {
  while (replayState.autoPlay && replayState.currentIndex < replayState.events.length - 1) {
    stepReplay(1);
    await new Promise((r) => setTimeout(r, 3000));
  }
}

function updateReplayView() {
  if (replayState.typingInterval) clearInterval(replayState.typingInterval);

  const event = replayState.events[replayState.currentIndex];
  if (!event) return;

  const progress =
    replayState.events.length > 1
      ? (replayState.currentIndex / (replayState.events.length - 1)) * 100
      : 100;

  document.getElementById("ia-progress-fill").style.width = `${progress}%`;
  document.getElementById("ia-meta").textContent = event.meta;
  document.getElementById("ia-actor-name").textContent = event.actor || "SYSTEM";

  // Typing effect
  const dialogText = document.getElementById("ia-dialog-text");
  dialogText.textContent = "";
  let i = 0;
  replayState.typingInterval = setInterval(() => {
    if (i < event.text.length) {
      dialogText.textContent += event.text.charAt(i);
      i++;
    } else {
      clearInterval(replayState.typingInterval);
    }
  }, 20);

  // Update nodes and suspicion
  const container = document.querySelector(".iarena-container");
  if (container) {
    container.classList.remove("day", "night");
    if (event.phase) container.classList.add(event.phase);
  }

  document.querySelectorAll(".ia-actor-node").forEach((n) => n.classList.remove("active", "glitch"));

  if (event.actor) {
    const node = document.getElementById(`node-${event.actor}`);
    if (node) {
      node.classList.add("active");
      if (event.isElimination) {
        node.classList.add("eliminated", "glitch");
        if (container) {
          container.classList.add("glitch");
          setTimeout(() => container.classList.remove("glitch"), 500);
        }
      }
    }

    // Heuristic suspicion: if someone accuses or votes, increase score slightly
    if (event.type === "ACTION" || event.text.toLowerCase().includes("acus") || event.text.toLowerCase().includes("sospech") || event.text.toLowerCase().includes("suspect")) {
      replayState.suspicionScores[event.actor] = Math.min(100, (replayState.suspicionScores[event.actor] || 0) + 15);
    }
  }

  // Update Suspicion Bars
  Object.keys(replayState.suspicionScores).forEach((p) => {
    const bar = document.getElementById(`susp-bar-${p}`);
    if (bar) {
      const score = replayState.suspicionScores[p];
      bar.style.width = `${score}%`;
      bar.classList.toggle("medium", score > 40);
      bar.classList.toggle("high", score > 75);
    }
  });

  // Final Reveal
  if (event.type === "REVEAL" && event.roles) {
    Object.keys(event.roles).forEach((pName) => {
      const role = event.roles[pName];
      const node = document.getElementById(`node-${pName}`);
      if (node) {
        node.style.borderColor = role === "werewolf" ? "var(--blood-alert)" : "var(--gb-phosphor)";
        node.style.color = role === "werewolf" ? "var(--blood-alert)" : "var(--gb-phosphor)";
        node.innerHTML = `<small style="font-size: 0.4rem">${t(role).toUpperCase()}</small><span>${pName}</span>`;
      }
    });
  }
}
