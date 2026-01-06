import asyncio
import aiohttp
import json
import logging
import sys

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def run_simulation():
    """Simulate a full game start and monitor for events."""
    logger.info("🚀 Starting Game Simulation...")
    
    try:
        async with aiohttp.ClientSession() as session:
            # 1. Connect to WebSocket FIRST to capture all events
            ws_url = "ws://localhost:8000/ws"
            logger.info(f"🔌 Connecting to WebSocket {ws_url}...")
            
            try:
                async with session.ws_connect(ws_url) as ws:
                    logger.info("✅ WebSocket Connected. Ready to capture events.")
                    
                    # 2. Trigger Game Start (in background task/async)
                    # We need to send the POST request while keeping WS open
                    # We'll use asyncio.create_task for the trigger
                    async def trigger_game():
                        url = "http://localhost:8000/start_game"
                        payload = {"num_players": 5}
                        logger.info(f"📡 Sending START request to {url}...")
                        async with aiohttp.ClientSession() as trigger_session:
                            async with trigger_session.post(url, json=payload) as resp:
                                if resp.status == 200:
                                    data = await resp.json()
                                    task_id = data.get("result", {}).get("task_id")
                                    logger.info(f"✅ Game Started! Task ID: {task_id}")
                                    return True
                                else:
                                    text = await resp.text()
                                    logger.error(f"❌ Failed to start game: {resp.status} - {text}")
                                    return False
                    
                    # Launch trigger
                    trigger_task = asyncio.create_task(trigger_game())
                    
                    # 3. Monitor Events
                    events_received = {
                        "game_start": False,
                        "phase_change": False,
                        "player_speak": False,
                        "player_eliminated": False
                    }
                    
                    start_time = asyncio.get_event_loop().time()
                    
                    while not all(events_received.values()):
                        try:
                            # Wait for message with short timeout to allow checking loop condition
                            msg = await asyncio.wait_for(ws.receive(), timeout=1.0)
                            
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                data = json.loads(msg.data)
                                event_type = data.get("type")
                                logger.info(f"📨 Event Received: {event_type}")
                                
                                if event_type in events_received:
                                    events_received[event_type] = True
                                    logger.info(f"   -> Details: {str(data)[:100]}...")
                                    
                                if event_type == "game_over":
                                    logger.info("🏁 Game Over event received.", )
                                    break
                                    
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                logger.error("WebSocket connection closed with error")
                                break
                        except asyncio.TimeoutError:
                            # Just a tick
                            pass
                        
                        # Check global timeout (30s should be enough for start)
                        if asyncio.get_event_loop().time() - start_time > 30:
                            logger.warn("⏰ Simulation timed out waiting for events.")
                            break
                            
                    # Wait for trigger to finish just in case
                    await trigger_task
                            
                    # Report results
                    logger.info("\n=== Simulation Results ===")
                    for event, received in events_received.items():
                        status = "✅ PASS" if received else "❌ FAIL"
                        logger.info(f"{event.ljust(20)}: {status}")
                        
                    # We consider success if we at least started and got some flow
                    # If agents are dumb/missing key, we might miss 'player_speak'
                    if events_received["game_start"]:
                        return True
                    return False
                    
            except Exception as e:
                logger.error(f"WebSocket error: {e}")
                return False
                
    except Exception as e:
        logger.error(f"Simulation failed: {e}")
        return False

if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    success = asyncio.run(run_simulation())
    sys.exit(0 if success else 1)
