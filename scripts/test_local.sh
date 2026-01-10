#!/bin/bash
# Quick local test script - NO API COSTS
# Uses dummy mode (random decisions) to test game flow

set -e

echo "=========================================="
echo "Werewolf Arena - Local Test (FREE)"
echo "=========================================="
echo ""
echo "This test uses 'dummy' mode - no API calls, no costs."
echo "Agents will make random decisions."
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "ERROR: Docker is not running. Please start Docker first."
    exit 1
fi

# Build and run with test configuration
echo "Building containers..."
docker compose -f docker-compose.test.yml build

echo ""
echo "Starting agents (dummy mode)..."
docker compose -f docker-compose.test.yml up -d

echo ""
echo "Waiting for agents to be ready..."
sleep 5

# Check if agents are running
echo ""
echo "Checking agent health..."

check_agent() {
    local url=$1
    local name=$2
    if curl -s "$url/.well-known/agent-card.json" > /dev/null 2>&1; then
        echo "  ✓ $name is ready"
        return 0
    else
        echo "  ✗ $name is not responding"
        return 1
    fi
}

check_agent "http://localhost:9009" "Green Agent (Evaluator)"
check_agent "http://localhost:9010" "Purple Agent 1"
check_agent "http://localhost:9011" "Purple Agent 2"
check_agent "http://localhost:9012" "Purple Agent 3"
check_agent "http://localhost:9013" "Purple Agent 4"
check_agent "http://localhost:9014" "Purple Agent 5"

echo ""
echo "=========================================="
echo "All agents are running!"
echo "=========================================="
echo ""
echo "To trigger a game:"
echo "  uv run python scripts/trigger_assessment.py"
echo ""
echo "To see logs:"
echo "  docker compose -f docker-compose.test.yml logs -f"
echo ""
echo "To stop:"
echo "  docker compose -f docker-compose.test.yml down"
echo ""
