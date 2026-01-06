import requests
import sys

def check_service(name, url):
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            print(f"✅ {name}: ONLINE ({url})")
            return True
        else:
            print(f"⚠️ {name}: ERROR {response.status_code} ({url})")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ {name}: UNREACHABLE ({url})")
        return False
    except Exception as e:
        print(f"❌ {name}: FAILED ({e})")
        return False

def main():
    print("=== Werewolf Arena Connection Check ===\n")
    
    # Check Green Agent (Server)
    server_ok = check_service("Green Agent (Server)", "http://localhost:8000/health")
    
    # Check Purple Agents (Players)
    agents_ok = 0
    for i in range(5):
        port = 8001 + i
        name = f"Purple Agent {i+1}"
        if check_service(name, f"http://localhost:{port}/health"):
            agents_ok += 1
            
    print("\n=== Summary ===")
    if server_ok and agents_ok == 5:
        print("🎉 SYSTEM READY: All components are online.")
        sys.exit(0)
    else:
        print(f"⚠️ SYSTEM ISSUES: Server={server_ok}, Agents={agents_ok}/5")
        sys.exit(1)

if __name__ == "__main__":
    main()
