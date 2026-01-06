# Copyright 2024 Google LLC
# Modifications for AgentBeats integration
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0

"""A2A Protocol Models - Pydantic schemas for Agent-to-Agent communication."""

from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import Enum


class MessageType(str, Enum):
    """Types of A2A messages."""
    ASSESSMENT_REQUEST = "assessment_request"
    ROLE_ASSIGNMENT = "role_assignment"
    ACTION_REQUEST = "action_request"
    ACTION_RESPONSE = "action_response"
    TASK_UPDATE = "task_update"
    ASSESSMENT_RESULT = "assessment_result"
    ERROR = "error"


class GamePhase(str, Enum):
    """Phases of the Werewolf game."""
    NIGHT = "night"
    DAY = "day"
    VOTING = "voting"
    ENDED = "ended"


class ActionType(str, Enum):
    """Types of player actions."""
    BID = "bid"
    DEBATE = "debate"
    VOTE = "vote"
    ELIMINATE = "eliminate"
    INVESTIGATE = "investigate"
    PROTECT = "protect"
    SUMMARIZE = "summarize"


class RoleType(str, Enum):
    """Player roles in Werewolf."""
    WEREWOLF = "werewolf"
    VILLAGER = "villager"
    SEER = "seer"
    DOCTOR = "doctor"


# ============ A2A Request/Response Models ============

class AssessmentConfig(BaseModel):
    """Configuration for an assessment."""
    num_players: int = Field(default=5, ge=5, le=8)
    max_rounds: int = Field(default=10, ge=1)
    timeout_seconds: int = Field(default=60, ge=10)
    debug: bool = Field(default=False)


class AssessmentRequest(BaseModel):
    """Initial assessment request from AgentBeats platform."""
    type: str = Field(default=MessageType.ASSESSMENT_REQUEST)
    task_id: str
    participants: Dict[str, str]  # player_name -> endpoint_url
    config: AssessmentConfig = Field(default_factory=AssessmentConfig)


class RoleAssignment(BaseModel):
    """Role assignment message sent to Purple Agent."""
    type: str = Field(default=MessageType.ROLE_ASSIGNMENT)
    task_id: str
    player_name: str
    role: RoleType
    role_description: str
    game_rules: str
    teammates: Optional[List[str]] = None  # For werewolves only


class GameState(BaseModel):
    """Current state of the game sent to players."""
    round: int
    phase: GamePhase
    alive_players: List[str]
    eliminated_players: List[str] = Field(default_factory=list)
    debate_so_far: List[Dict[str, str]] = Field(default_factory=list)
    announcements: List[str] = Field(default_factory=list)
    your_observations: List[str] = Field(default_factory=list)


class ActionRequest(BaseModel):
    """Request for a player to take an action."""
    type: str = Field(default=MessageType.ACTION_REQUEST)
    task_id: str
    player_name: str
    action: ActionType
    game_state: GameState
    options: Optional[List[str]] = None  # Valid choices for the action
    context: Optional[str] = None  # Additional context for the action


class ActionResponse(BaseModel):
    """Player's response to an action request."""
    type: str = Field(default=MessageType.ACTION_RESPONSE)
    task_id: str
    player_name: str
    action: ActionType
    decision: str
    reasoning: Optional[str] = None


class TaskUpdate(BaseModel):
    """Progress update emitted during assessment."""
    type: str = Field(default=MessageType.TASK_UPDATE)
    task_id: str
    message: str
    round: Optional[int] = None
    phase: Optional[GamePhase] = None
    details: Optional[Dict[str, Any]] = None


class PlayerScore(BaseModel):
    """Individual player's score."""
    player_name: str
    role: RoleType
    team: str  # "werewolves" or "villagers"
    won: bool
    survived: bool
    metrics: Dict[str, float] = Field(default_factory=dict)
    elo_delta: Optional[float] = None


class AssessmentResult(BaseModel):
    """Final assessment result artifact."""
    type: str = Field(default=MessageType.ASSESSMENT_RESULT)
    task_id: str
    winner: str  # "werewolves" or "villagers"
    rounds_played: int
    game_log: List[Dict[str, Any]] = Field(default_factory=list)
    scores: List[PlayerScore] = Field(default_factory=list)
    aggregate_metrics: Dict[str, float] = Field(default_factory=dict)


class ErrorMessage(BaseModel):
    """Error message for failed operations."""
    type: str = Field(default=MessageType.ERROR)
    task_id: str
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None


# ============ Agent Card Models ============

class AgentCapabilities(BaseModel):
    """Agent capabilities descriptor."""
    roles: List[str] = Field(default_factory=lambda: ["evaluator"])
    protocols: List[str] = Field(default_factory=lambda: ["a2a"])


class AssessmentSpec(BaseModel):
    """Assessment specification for Green Agent."""
    min_participants: int = 5
    max_participants: int = 8
    supported_roles: List[str] = Field(
        default_factory=lambda: ["werewolf", "villager", "seer", "doctor"]
    )


class AgentCard(BaseModel):
    """A2A Agent Card descriptor."""
    name: str
    description: str
    version: str
    url: str
    capabilities: AgentCapabilities = Field(default_factory=AgentCapabilities)
    assessment: Optional[AssessmentSpec] = None


# ============ A2A Envelope ============

class A2AMessage(BaseModel):
    """Generic A2A message envelope."""
    jsonrpc: str = "2.0"
    method: str
    params: Dict[str, Any] = Field(default_factory=dict)
    id: Optional[str] = None


class A2AResponse(BaseModel):
    """Generic A2A response envelope."""
    jsonrpc: str = "2.0"
    result: Optional[Dict[str, Any]] = None
    error: Optional[Dict[str, Any]] = None
    id: Optional[str] = None
