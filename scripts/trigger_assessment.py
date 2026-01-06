#!/usr/bin/env python3
# Copyright 2024 Google LLC
# Modifications for AgentBeats integration
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0

"""
Trigger an assessment on the local Green Agent.

Usage:
    python scripts/trigger_assessment.py

This script sends an assessment request to the Green Agent with
multiple Purple Agents and monitors the game progress.
"""

import argparse
import asyncio
import json
import sys
import time
from typing import Dict, Any

import httpx


async def trigger_assessment(
    green_url: str,
    participants: Dict[str, str],
    config: Dict[str, Any],
) -> str:
    """Send assessment request and return task_id."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        request = {
            "jsonrpc": "2.0",
            "method": "assessment_request",
            "params": {
                "participants": participants,
                "config": config,
            },
            "id": "trigger_1",
        }
        
        print(f"Sending assessment request to {green_url}/a2a")
        print(f"Participants: {list(participants.keys())}")
        
        response = await client.post(
            f"{green_url}/a2a",
            json=request,
        )
        response.raise_for_status()
        
        result = response.json()
        if "error" in result and result["error"]:
            raise Exception(f"Assessment error: {result['error']}")
        
        task_id = result.get("result", {}).get("task_id")
        print(f"Assessment started with task_id: {task_id}")
        return task_id


async def poll_status(green_url: str, task_id: str, interval: float = 2.0):
    """Poll assessment status until complete."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        while True:
            request = {
                "jsonrpc": "2.0",
                "method": "get_status",
                "params": {"task_id": task_id},
                "id": "poll_1",
            }
            
            response = await client.post(
                f"{green_url}/a2a",
                json=request,
            )
            try:
                data = response.json()
            except Exception as e:
                print(f"Error parsing JSON: {response.text}")
                raise e

            if data.get("error"):
                print(f"API Error: {data['error']}")
                raise Exception(f"API Error: {data['error']}")

            result = data.get("result", {})
            if result is None:
                print(f"No result in data: {data}")
                result = {}
            
            status = result.get("status", "unknown")
            
            if status == "completed":
                print(f"\n✅ Assessment completed!")
                print(f"   Winner: {result.get('winner', 'unknown')}")
                return result
            
            if status == "running":
                round_num = result.get("round", "?")
                phase = result.get("phase", "?")
                latest = result.get("latest_update", "")[:50]
                print(f"   Round {round_num} - {phase}: {latest}...")
            else:
                print(f"   Status: {status}")
            
            await asyncio.sleep(interval)


async def get_result(green_url: str, task_id: str) -> Dict[str, Any]:
    """Get final assessment result."""
    async with httpx.AsyncClient(timeout=30.0) as client:
        request = {
            "jsonrpc": "2.0",
            "method": "get_result",
            "params": {"task_id": task_id},
            "id": "result_1",
        }
        
        response = await client.post(
            f"{green_url}/a2a",
            json=request,
        )
        return response.json().get("result", {})


async def main():
    parser = argparse.ArgumentParser(description="Trigger a Werewolf assessment")
    parser.add_argument(
        "--green-url",
        default="http://localhost:8000",
        help="URL of the Green Agent",
    )
    parser.add_argument(
        "--num-players",
        type=int,
        default=5,
        help="Number of players (5-8)",
    )
    parser.add_argument(
        "--base-port",
        type=int,
        default=8001,
        help="Base port for Purple Agents",
    )
    parser.add_argument(
        "--max-rounds",
        type=int,
        default=10,
        help="Maximum number of game rounds",
    )
    parser.add_argument(
        "--output",
        help="File to save results JSON",
    )
    
    args = parser.parse_args()
    
    # Build participants
    participants = {
        f"player_{i+1}": f"http://localhost:{args.base_port + i}"
        for i in range(args.num_players)
    }
    
    # For docker-compose, use container names
    # participants = {
    #     "player_1": "http://purple-agent-1:8001",
    #     "player_2": "http://purple-agent-2:8002",
    #     ...
    # }
    
    config = {
        "num_players": args.num_players,
        "max_rounds": args.max_rounds,
        "timeout_seconds": 60,
    }
    
    print("=" * 60)
    print("🐺 Werewolf Arena - Assessment Trigger")
    print("=" * 60)
    
    try:
        # Trigger assessment
        task_id = await trigger_assessment(
            args.green_url,
            participants,
            config,
        )
        
        print("\n📊 Polling status...")
        await poll_status(args.green_url, task_id)
        
        print("\n📋 Getting full results...")
        result = await get_result(args.green_url, task_id)
        
        # Print summary
        print("\n" + "=" * 60)
        print("📊 ASSESSMENT RESULTS")
        print("=" * 60)
        print(f"Winner: {result.get('winner', 'unknown')}")
        print(f"Rounds: {result.get('rounds_played', 0)}")
        
        if "scores" in result:
            print("\nPlayer Scores:")
            for score in result["scores"]:
                name = score.get("player_name", "?")
                role = score.get("role", "?")
                won = "✅" if score.get("won") else "❌"
                survived = "💚" if score.get("survived") else "💀"
                agg = score.get("metrics", {}).get("aggregate_score", 0)
                print(f"  {name} ({role}): {won} {survived} Score: {agg:.2f}")
        
        # Save to file if requested
        if args.output:
            with open(args.output, "w") as f:
                json.dump(result, f, indent=2)
            print(f"\n💾 Results saved to {args.output}")
        
        print("\n✅ Assessment complete!")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
