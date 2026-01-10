"""A2A Conformance tests for Werewolf Arena Green Agent."""

import httpx
import pytest


class TestGreenAgentCard:
    """Test the A2A agent card endpoint."""

    def test_agent_card_endpoint_exists(self, green_agent_url):
        """Test that /.well-known/agent-card.json endpoint exists."""
        response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        assert response.status_code == 200

    def test_agent_card_has_required_fields(self, green_agent_url):
        """Test that agent card has all required A2A fields."""
        response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        card = response.json()

        # Required fields per A2A spec
        assert "name" in card, "Agent card must have 'name'"
        assert "description" in card, "Agent card must have 'description'"
        assert "version" in card, "Agent card must have 'version'"
        assert "url" in card, "Agent card must have 'url'"

    def test_agent_card_has_skills(self, green_agent_url):
        """Test that agent card has skills array."""
        response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        card = response.json()

        assert "skills" in card, "Agent card must have 'skills'"
        assert isinstance(card["skills"], list), "Skills must be a list"
        assert len(card["skills"]) > 0, "Agent must have at least one skill"

        # Check skill structure
        skill = card["skills"][0]
        assert "id" in skill, "Skill must have 'id'"
        assert "name" in skill, "Skill must have 'name'"

    def test_agent_card_has_capabilities(self, green_agent_url):
        """Test that agent card has capabilities."""
        response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        card = response.json()

        assert "capabilities" in card, "Agent card must have 'capabilities'"

    def test_agent_card_has_input_output_modes(self, green_agent_url):
        """Test that agent card specifies input/output modes."""
        response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        card = response.json()

        assert "default_input_modes" in card, "Agent card should have 'default_input_modes'"
        assert "default_output_modes" in card, "Agent card should have 'default_output_modes'"


class TestGreenAgentHealth:
    """Test the health endpoint."""

    def test_health_endpoint_exists(self, green_agent_url):
        """Test that /health endpoint exists."""
        response = httpx.get(f"{green_agent_url}/health")
        assert response.status_code == 200

    def test_health_returns_status(self, green_agent_url):
        """Test that health endpoint returns status."""
        response = httpx.get(f"{green_agent_url}/health")
        data = response.json()

        assert "status" in data, "Health response must have 'status'"
        assert data["status"] == "healthy", "Status should be 'healthy'"


class TestGreenAgentA2A:
    """Test the A2A protocol endpoint."""

    def test_a2a_endpoint_exists(self, green_agent_url):
        """Test that /a2a endpoint exists."""
        response = httpx.post(
            f"{green_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "unknown_method",
                "params": {},
                "id": "test-1",
            },
        )
        # Should return error for unknown method, but not 404
        assert response.status_code == 200

    def test_a2a_returns_jsonrpc_response(self, green_agent_url):
        """Test that A2A endpoint returns JSON-RPC format."""
        response = httpx.post(
            f"{green_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "get_status",
                "params": {"task_id": "nonexistent"},
                "id": "test-2",
            },
        )
        data = response.json()

        assert "jsonrpc" in data, "Response must have 'jsonrpc'"
        assert data["jsonrpc"] == "2.0", "JSON-RPC version must be 2.0"

    def test_a2a_assessment_request_validation(self, green_agent_url):
        """Test that assessment request validates participant count."""
        response = httpx.post(
            f"{green_agent_url}/a2a",
            json={
                "jsonrpc": "2.0",
                "method": "assessment_request",
                "params": {
                    "task_id": "test-validation",
                    "participants": {"player_1": "http://localhost:9010"},  # Only 1 participant
                    "config": {},
                },
                "id": "test-3",
            },
        )
        data = response.json()

        # Should return error because minimum is 5 participants
        assert "error" in data, "Should return error for insufficient participants"


class TestGreenAgentInfo:
    """Test the /info endpoint (legacy)."""

    def test_info_endpoint_exists(self, green_agent_url):
        """Test that /info endpoint exists."""
        response = httpx.get(f"{green_agent_url}/info")
        assert response.status_code == 200

    def test_info_returns_same_as_agent_card(self, green_agent_url):
        """Test that /info returns same content as agent-card.json."""
        card_response = httpx.get(f"{green_agent_url}/.well-known/agent-card.json")
        info_response = httpx.get(f"{green_agent_url}/info")

        assert card_response.json() == info_response.json()
