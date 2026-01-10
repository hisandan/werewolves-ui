"""A2A Conformance tests for Werewolf Arena Purple Agent."""

import httpx
import pytest


class TestPurpleAgentCard:
    """Test the A2A agent card endpoint."""

    def test_agent_card_endpoint_exists(self, purple_agent_url):
        """Test that /.well-known/agent-card.json endpoint exists."""
        response = httpx.get(f"{purple_agent_url}/.well-known/agent-card.json")
        assert response.status_code == 200

    def test_agent_card_has_required_fields(self, purple_agent_url):
        """Test that agent card has all required A2A fields."""
        response = httpx.get(f"{purple_agent_url}/.well-known/agent-card.json")
        card = response.json()

        # Required fields per A2A spec
        assert "name" in card, "Agent card must have 'name'"
        assert "description" in card, "Agent card must have 'description'"
        assert "version" in card, "Agent card must have 'version'"
        assert "url" in card, "Agent card must have 'url'"

    def test_agent_card_has_skills(self, purple_agent_url):
        """Test that agent card has skills array."""
        response = httpx.get(f"{purple_agent_url}/.well-known/agent-card.json")
        card = response.json()

        assert "skills" in card, "Agent card must have 'skills'"
        assert isinstance(card["skills"], list), "Skills must be a list"
        assert len(card["skills"]) > 0, "Agent must have at least one skill"

    def test_agent_card_has_supported_roles(self, purple_agent_url):
        """Test that agent card specifies supported game roles."""
        response = httpx.get(f"{purple_agent_url}/.well-known/agent-card.json")
        card = response.json()

        assert "capabilities" in card
        caps = card["capabilities"]
        assert "supported_game_roles" in caps, "Purple agent should specify supported game roles"

        roles = caps["supported_game_roles"]
        assert "werewolf" in roles
        assert "villager" in roles


class TestPurpleAgentHealth:
    """Test the health endpoint."""

    def test_health_endpoint_exists(self, purple_agent_url):
        """Test that /health endpoint exists."""
        response = httpx.get(f"{purple_agent_url}/health")
        assert response.status_code == 200

    def test_health_returns_status(self, purple_agent_url):
        """Test that health endpoint returns status."""
        response = httpx.get(f"{purple_agent_url}/health")
        data = response.json()

        assert "status" in data, "Health response must have 'status'"
        assert data["status"] == "healthy", "Status should be 'healthy'"


class TestPurpleAgentA2A:
    """Test the A2A protocol endpoint."""

    def test_a2a_endpoint_exists(self, purple_agent_url):
        """Test that /a2a endpoint exists."""
        response = httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "unknown_method",
                "params": {},
                "id": "test-1",
            },
        )
        # Should return error for unknown method, but not 404
        assert response.status_code == 200

    def test_a2a_returns_jsonrpc_response(self, purple_agent_url):
        """Test that A2A endpoint returns JSON-RPC format."""
        response = httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "reset",
                "params": {},
                "id": "test-2",
            },
        )
        data = response.json()

        assert "jsonrpc" in data, "Response must have 'jsonrpc'"
        assert data["jsonrpc"] == "2.0", "JSON-RPC version must be 2.0"

    def test_a2a_role_assignment(self, purple_agent_url):
        """Test role assignment A2A method."""
        # First reset the agent
        httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "reset",
                "params": {},
                "id": "reset-1",
            },
        )

        # Then assign a role
        response = httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "role_assignment",
                "params": {
                    "task_id": "test-game-1",
                    "player_name": "TestPlayer",
                    "role": "villager",
                    "role_description": "You are a villager. Find the werewolves!",
                    "game_rules": "Standard Werewolf rules",
                },
                "id": "assign-1",
            },
        )
        data = response.json()

        assert "result" in data, "Role assignment should return result"
        assert data["result"]["status"] == "ok"

    def test_a2a_action_request_without_role(self, purple_agent_url):
        """Test that action request fails without role assignment."""
        # Reset first to clear any existing state
        httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "reset",
                "params": {},
                "id": "reset-2",
            },
        )

        # Try to take action without role
        response = httpx.post(
            f"{purple_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "action_request",
                "params": {
                    "action": "debate",
                    "game_state": {
                        "round": 1,
                        "phase": "day",
                        "alive_players": ["Player1", "Player2"],
                    },
                },
                "id": "action-1",
            },
        )
        data = response.json()

        # Should return error because role not assigned
        assert "error" in data, "Should return error when role not assigned"


class TestPurpleAgentState:
    """Test the state endpoint."""

    def test_state_endpoint_exists(self, purple_agent_url):
        """Test that /state endpoint exists."""
        response = httpx.get(f"{purple_agent_url}/state")
        assert response.status_code == 200


class TestPurpleAgentInfo:
    """Test the /info endpoint (legacy)."""

    def test_info_endpoint_exists(self, purple_agent_url):
        """Test that /info endpoint exists."""
        response = httpx.get(f"{purple_agent_url}/info")
        assert response.status_code == 200

    def test_info_returns_same_as_agent_card(self, purple_agent_url):
        """Test that /info returns same content as agent-card.json."""
        card_response = httpx.get(f"{purple_agent_url}/.well-known/agent-card.json")
        info_response = httpx.get(f"{purple_agent_url}/info")

        assert card_response.json() == info_response.json()
