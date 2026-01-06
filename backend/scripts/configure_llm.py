#!/usr/bin/env python3
"""
Configurador interactivo de LLM para Werewolf Arena.

Soporta:
- LM Studio (local)
- Ollama (local)  
- OpenRouter (cloud)
- Gemini (via OpenAI compat)

Uso:
    python configure_llm.py
"""

import os
import sys

# Colores para la terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_banner():
    print(f"""
{Colors.CYAN}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════╗
║          🐺 WEREWOLF ARENA - Configurador de LLM 🐺          ║
╠══════════════════════════════════════════════════════════════╣
║  Selecciona el proveedor de LLM para los agentes jugadores  ║
╚══════════════════════════════════════════════════════════════╝
{Colors.END}
""")

def print_menu():
    print(f"""
{Colors.BOLD}Proveedores disponibles:{Colors.END}

  {Colors.GREEN}[1]{Colors.END} 💻 LM Studio (Local)
      • URL: http://localhost:1234/v1
      • Gratis, privado, sin límites
      • Requiere: LM Studio corriendo
      
  {Colors.YELLOW}[2]{Colors.END} 🦙 Ollama (Local)
      • URL: http://localhost:11434/v1
      • Gratis, fácil de usar
      • Requiere: ollama serve
      
  {Colors.BLUE}[3]{Colors.END} 🌐 OpenRouter (Cloud)
      • URL: https://openrouter.ai/api/v1
      • Muchos modelos disponibles
      • Requiere: API key de OpenRouter

  {Colors.HEADER}[4]{Colors.END} ✨ Gemeni / Google (Cloud)
      • URL: https://generativelanguage.googleapis.com/v1beta/openai/
      • Rápido y con tier gratuito
      • Requiere: API key de Google AI Studio
      
  {Colors.CYAN}[5]{Colors.END} ⚙️  Configuración personalizada
      • Define tu propia URL y modelo
      
  {Colors.RED}[0]{Colors.END} ❌ Salir

""")

PROVIDERS = {
    "1": {
        "name": "LM Studio",
        "base_url": "http://localhost:1234/v1",
        "api_key": "lmstudio",
        "default_model": "local-model",
        "needs_api_key": False,
    },
    "2": {
        "name": "Ollama", 
        "base_url": "http://localhost:11434/v1",
        "api_key": "ollama",
        "default_model": "llama3.2",
        "needs_api_key": False,
    },
    "3": {
        "name": "OpenRouter",
        "base_url": "https://openrouter.ai/api/v1",
        "api_key": "",
        "default_model": "meta-llama/llama-3.2-3b-instruct:free",
        "needs_api_key": True,
    },
    "4": {
        "name": "Gemini",
        "base_url": "https://generativelanguage.googleapis.com/v1beta/openai/",
        "api_key": "",
        "default_model": "gemini-1.5-flash",
        "needs_api_key": True,
    }
}

def get_ollama_models():
    """Intenta obtener modelos disponibles en Ollama."""
    try:
        import httpx
        response = httpx.get("http://localhost:11434/api/tags", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return [m["name"] for m in data.get("models", [])]
    except ImportError:
        print(f"{Colors.RED}Error: httpx no instalado. Ejecuta 'pip install httpx'{Colors.END}")
        return []
    except:
        pass
    return []

def get_lmstudio_models():
    """Intenta obtener modelos disponibles en LM Studio."""
    try:
        import httpx
        response = httpx.get("http://localhost:1234/v1/models", timeout=3)
        if response.status_code == 200:
            data = response.json()
            return [m["id"] for m in data.get("data", [])]
    except ImportError:
        return []
    except:
        pass
    return []

def configure_lmstudio():
    print(f"\n{Colors.GREEN}=== Configuración de LM Studio ==={Colors.END}\n")
    
    models = get_lmstudio_models()
    if models:
        print(f"Modelos detectados en LM Studio:")
        for i, m in enumerate(models, 1):
            print(f"  [{i}] {m}")
        print()
        choice = input("Selecciona modelo (Enter para usar el primero): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        return models[0]
    else:
        print(f"{Colors.YELLOW}⚠️  No se detectaron modelos. ¿LM Studio está corriendo?{Colors.END}")
        model = input("Nombre del modelo (Enter para 'local-model'): ").strip()
        return model or "local-model"

def configure_ollama():
    print(f"\n{Colors.YELLOW}=== Configuración de Ollama ==={Colors.END}\n")
    
    models = get_ollama_models()
    if models:
        print(f"Modelos disponibles en Ollama:")
        for i, m in enumerate(models, 1):
            print(f"  [{i}] {m}")
        print()
        choice = input("Selecciona modelo (Enter para usar el primero): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(models):
            return models[int(choice) - 1]
        return models[0]
    else:
        print(f"{Colors.YELLOW}⚠️  No se detectaron modelos.{Colors.END}")
        print("Ejecuta: ollama pull llama3.2")
        model = input("Nombre del modelo (Enter para 'llama3.2'): ").strip()
        return model or "llama3.2"

def configure_openrouter():
    print(f"\n{Colors.BLUE}=== Configuración de OpenRouter ==={Colors.END}\n")
    
    print("Modelos gratuitos recomendados:")
    print("  [1] meta-llama/llama-3.2-3b-instruct:free")
    print("  [2] google/gemma-2-9b-it:free")
    print("  [3] mistralai/mistral-7b-instruct:free")
    print()
    
    api_key = input("API Key de OpenRouter (sk-or-...): ").strip()
    if not api_key:
        print(f"{Colors.RED}❌ Se requiere API key para OpenRouter{Colors.END}")
        return None, None
    
    model_choice = input("Modelo [1-3] o nombre personalizado (Enter para 1): ").strip()
    
    models = {
        "1": "meta-llama/llama-3.2-3b-instruct:free",
        "2": "google/gemma-2-9b-it:free",
        "3": "mistralai/mistral-7b-instruct:free",
    }
    
    model = models.get(model_choice, model_choice) or models["1"]
    
    return api_key, model

def configure_gemini():
    print(f"\n{Colors.HEADER}=== Configuración de Gemini ==={Colors.END}\n")
    
    print("Modelos recomendados:")
    print("  [1] gemini-1.5-flash")
    print("  [2] gemini-1.5-flash-001")
    print("  [3] gemini-1.5-pro")
    print()
    
    api_key = input("API Key de Google AI Studio: ").strip()
    if not api_key:
        print(f"{Colors.RED}❌ Se requiere API key{Colors.END}")
        return None, None
    
    model_choice = input("Modelo [1-3] o nombre personalizado (Enter para 1): ").strip()
    
    models = {
        "1": "gemini-1.5-flash",
        "2": "gemini-1.5-flash-001",
        "3": "gemini-1.5-pro",
    }
    
    model = models.get(model_choice, model_choice) or models["1"]
    
    return api_key, model

def configure_custom():
    print(f"\n{Colors.CYAN}=== Configuración Personalizada ==={Colors.END}\n")
    
    base_url = input("Base URL (ej: http://localhost:8080/v1): ").strip()
    if not base_url:
        print(f"{Colors.RED}❌ Se requiere URL{Colors.END}")
        return None
    
    api_key = input("API Key (Enter para 'custom'): ").strip() or "custom"
    model = input("Nombre del modelo: ").strip() or "default"
    
    return {
        "base_url": base_url,
        "api_key": api_key,
        "model": model,
    }

def write_env_file(base_url: str, api_key: str, model: str):
    """Escribe el archivo .env con la configuración adaptada para Werewolf Arena."""
    
    env_content = f"""# Werewolf Arena Assessor - LLM Configuration
# Generado automáticamente por configure_llm.py

# LLM Provider Settings
OPENAI_API_BASE={base_url}
OPENAI_API_KEY={api_key}
LLM_MODEL={model}

# Server Configuration (Defaults)
# HOST=0.0.0.0
# PORT=8000
"""
    
    try:
        with open("backend/.env", "w") as f:
            f.write(env_content)
    except FileNotFoundError:
        # Fallback if running from backend dir
        with open(".env", "w") as f:
            f.write(env_content)
    except Exception as e:
        print(f"{Colors.RED}Error al escribir .env: {e}{Colors.END}")

def test_connection(base_url: str, api_key: str, model: str):
    """Prueba la conexión al proveedor de LLM."""
    print(f"\n{Colors.CYAN}🔄 Probando conexión...{Colors.END}")
    
    try:
        import httpx
        
        # Intentar listar modelos o una llamada dummy simple de chat
        # Nota: Algunos providers (Gemini) pueden fallar en /models, así que intentamos un health check básico
        # Para simplificar, intentamos /models primero
        
        headers = {}
        if api_key:
            headers["Authorization"] = f"Bearer {api_key}"
            
        print(f"   Consultando {base_url}...")
        
        # Clean url for proper endpoint construction if needed, mostly user input sanitization
        if not base_url.endswith("/"):
            base_url += "/"
            
        # Try a simple models list first if standard OpenAI
        try:
            response = httpx.get(
                f"{base_url}models",
                headers=headers,
                timeout=10
            )
            if response.status_code == 200:
                print(f"{Colors.GREEN}✅ Conexión exitosa! (Models list OK){Colors.END}")
                return True
        except:
            pass
            
        # Fallback: asumimos que si no falló DNS/Connect, está "ok" para guardar
        # Realmente validar la key requeriría una call de chat, que cuesta dinero/quota
        
    except ImportError:
        print(f"{Colors.YELLOW}⚠️  httpx no instalado, saltando prueba de conexión.{Colors.END}")
    except Exception as e:
        print(f"{Colors.RED}❌ Error en prueba de conexión: {e}{Colors.END}")
    
    return False

def main():
    clear_screen()
    print_banner()
    print_menu()
    
    choice = input(f"{Colors.BOLD}Selecciona una opción [0-5]: {Colors.END}").strip()
    
    if choice == "0":
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    
    base_url = ""
    api_key = ""
    model = ""
    provider_name = ""
    
    if choice == "1":  # LM Studio
        provider = PROVIDERS["1"]
        base_url = provider["base_url"]
        api_key = provider["api_key"]
        model = configure_lmstudio()
        provider_name = "LM Studio"
        
    elif choice == "2":  # Ollama
        provider = PROVIDERS["2"]
        base_url = provider["base_url"]
        api_key = provider["api_key"]
        model = configure_ollama()
        provider_name = "Ollama"
        
    elif choice == "3":  # OpenRouter
        provider = PROVIDERS["3"]
        base_url = provider["base_url"]
        api_key, model = configure_openrouter()
        if not api_key:
            sys.exit(1)
        provider_name = "OpenRouter"

    elif choice == "4":  # Gemini
        provider = PROVIDERS["4"]
        base_url = provider["base_url"]
        api_key, model = configure_gemini()
        if not api_key:
            sys.exit(1)
        provider_name = "Gemini"
        
    elif choice == "5":  # Custom
        config = configure_custom()
        if not config:
            sys.exit(1)
        base_url = config["base_url"]
        api_key = config["api_key"]
        model = config["model"]
        provider_name = "Custom"
        
    else:
        print(f"{Colors.RED}❌ Opción inválida{Colors.END}")
        sys.exit(1)
    
    # Mostrar resumen
    print(f"""
{Colors.GREEN}╔══════════════════════════════════════════════════════════════╗
║                    📋 RESUMEN DE CONFIGURACIÓN               ║
╠══════════════════════════════════════════════════════════════╣{Colors.END}
  Proveedor: {Colors.BOLD}{provider_name}{Colors.END}
  URL:       {base_url}
  Modelo:    {model}
  API Key:   {'*' * min(len(api_key), 20)}...
{Colors.GREEN}╚══════════════════════════════════════════════════════════════╝{Colors.END}
""")
    
    # Probar conexión - Warning, this might block if httpx missing but we handled it
    # test_connection(base_url, api_key, model) 
    # (Comentado para evitar overhead en entorno de usuario si no es necesario)

    # Confirmar
    confirm = input(f"\n¿Guardar esta configuración? [S/n]: ").strip().lower()
    if confirm in ("", "s", "si", "sí", "y", "yes"):
        write_env_file(base_url, api_key, model)
        print(f"""
{Colors.GREEN}✅ Configuración guardada en .env{Colors.END}

{Colors.BOLD}Próximos pasos:{Colors.END}
  1. Reinicia los agentes si están corriendo:
     {Colors.YELLOW}.\\stop_local_game.ps1{Colors.END}
     {Colors.GREEN}.\\start_local_game.ps1{Colors.END}
""")
    else:
        print("\n❌ Configuración cancelada")

if __name__ == "__main__":
    main()
