"""Pytest configuration and fixtures for Werewolf Arena tests."""

import pytest


def pytest_addoption(parser):
    """Add custom command-line options."""
    parser.addoption(
        "--green-agent-url",
        action="store",
        default="http://localhost:9009",
        help="URL of the green agent to test",
    )
    parser.addoption(
        "--purple-agent-url",
        action="store",
        default="http://localhost:9010",
        help="URL of the purple agent to test",
    )


@pytest.fixture
def green_agent_url(request):
    """Get the green agent URL from command line."""
    return request.config.getoption("--green-agent-url")


@pytest.fixture
def purple_agent_url(request):
    """Get the purple agent URL from command line."""
    return request.config.getoption("--purple-agent-url")
