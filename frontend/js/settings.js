function selectProvider(provider) {
    document.querySelectorAll('.provider-card').forEach(c => c.classList.remove('selected'));
    document.querySelector(`.provider-card[data-provider="${provider}"]`).classList.add('selected');

    const config = configs[provider];
    document.getElementById('config-base-url').value = config.url;
    document.getElementById('config-api-key').value = config.key || '';
    document.getElementById('config-model').value = config.model;
}

const configs = {
    lmstudio: { url: 'http://localhost:1234/v1', key: 'lmstudio', model: 'local-model' },
    ollama: { url: 'http://localhost:11434/v1', key: 'ollama', model: 'llama3.2' },
    gemini: { url: 'https://generativelanguage.googleapis.com/v1beta/openai/', key: '', model: 'gemini-1.5-flash' },
    openrouter: { url: 'https://openrouter.ai/api/v1', key: '', model: 'meta-llama/llama-3.2-3b-instruct:free' }
};

async function saveConfiguration() {
    const url = document.getElementById('config-base-url').value;
    const key = document.getElementById('config-api-key').value;
    const model = document.getElementById('config-model').value;

    try {
        const res = await fetch('http://localhost:8000/config', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                OPENAI_API_BASE: url,
                OPENAI_API_KEY: key,
                LLM_MODEL: model
            })
        });

        if (res.ok) {
            alert('Configuration saved!');
        } else {
            alert('Error saving configuration');
        }
    } catch (e) {
        alert('Connection error: ' + e.message);
    }
}

// Select default
document.addEventListener('DOMContentLoaded', () => {
    // Add click listeners to cards
    document.querySelectorAll('.provider-card').forEach(card => {
        card.addEventListener('click', () => selectProvider(card.getAttribute('data-provider')));
    });
});
