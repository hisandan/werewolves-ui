# Copyright 2024 Google LLC
# Modifications for AgentBeats integration
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0

"""Multi-dimensional scoring system for Werewolf assessments."""

import math
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, field

from green_agent.models import RoleType, PlayerScore, ParticipantResult


@dataclass
class PlayerMetrics:
    """Metrics tracked for each player during a game."""
    player_name: str
    role: RoleType
    team: str  # "werewolves" or "villagers"
    
    # Game outcome
    won: bool = False
    survived: bool = False
    rounds_survived: int = 0
    
    # Action counts
    total_debates: int = 0
    total_votes: int = 0
    correct_votes: int = 0  # Votes against actual enemies
    wrong_votes: int = 0    # Votes against teammates
    
    # Influence tracking
    times_voted_against: int = 0
    successful_accusations: int = 0  # Led to enemy elimination
    failed_accusations: int = 0      # Led to teammate elimination
    
    # Role-specific metrics
    investigations_correct: int = 0  # Seer only
    investigations_total: int = 0    # Seer only
    protections_successful: int = 0  # Doctor only
    protections_total: int = 0       # Doctor only
    eliminations_successful: int = 0 # Werewolf only
    
    # Deception/Detection
    times_suspected_correctly: int = 0  # How many correctly accused them
    times_suspected_wrongly: int = 0    # How many wrongly accused them
    
    # Sabotage detection
    sabotage_actions: int = 0  # Actions that hurt own team
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "player_name": self.player_name,
            "role": self.role.value if isinstance(self.role, RoleType) else self.role,
            "team": self.team,
            "won": self.won,
            "survived": self.survived,
            "rounds_survived": self.rounds_survived,
            "total_debates": self.total_debates,
            "total_votes": self.total_votes,
            "correct_votes": self.correct_votes,
            "wrong_votes": self.wrong_votes,
            "times_voted_against": self.times_voted_against,
            "successful_accusations": self.successful_accusations,
            "failed_accusations": self.failed_accusations,
            "investigations_correct": self.investigations_correct,
            "investigations_total": self.investigations_total,
            "protections_successful": self.protections_successful,
            "protections_total": self.protections_total,
            "eliminations_successful": self.eliminations_successful,
            "times_suspected_correctly": self.times_suspected_correctly,
            "times_suspected_wrongly": self.times_suspected_wrongly,
            "sabotage_actions": self.sabotage_actions,
        }


class ScoringEngine:
    """Calculate multi-dimensional scores for players."""
    
    # Score weights
    WEIGHTS = {
        "win_rate": 0.30,
        "survival_rate": 0.15,
        "deception_score": 0.20,  # Werewolves
        "detection_score": 0.20,  # Villagers
        "influence_score": 0.15,
        "consistency_score": 0.10,
        "sabotage_penalty": -0.20,
    }
    
    # ELO constants
    ELO_K_FACTOR = 32
    ELO_INITIAL = 1000

    def __init__(self):
        # General ELO ratings
        self.elo_ratings: Dict[str, float] = {}
        # Role-specific ELO ratings
        self.werewolf_elo: Dict[str, float] = {}
        self.villager_elo: Dict[str, float] = {}
        # Accumulated metrics per participant (for multi-game aggregation)
        self.participant_stats: Dict[str, Dict[str, Any]] = {}
    
    def calculate_win_score(self, metrics: PlayerMetrics) -> float:
        """Calculate win-based score (0-1)."""
        return 1.0 if metrics.won else 0.0
    
    def calculate_survival_score(
        self,
        metrics: PlayerMetrics,
        total_rounds: int,
    ) -> float:
        """Calculate survival-based score (0-1)."""
        if total_rounds == 0:
            return 0.0
        base = metrics.rounds_survived / total_rounds
        bonus = 0.3 if metrics.survived else 0.0
        return min(1.0, base + bonus)
    
    def calculate_deception_score(self, metrics: PlayerMetrics) -> float:
        """Calculate deception score for werewolves (0-1)."""
        if metrics.team != "werewolves":
            return 0.0
        
        score = 0.0
        
        # Survived longer = better deception
        if metrics.survived:
            score += 0.4
        
        # Fewer correct suspicions against them = better
        total_suspicions = metrics.times_suspected_correctly + metrics.times_suspected_wrongly
        if total_suspicions > 0:
            deception_ratio = metrics.times_suspected_wrongly / total_suspicions
            score += 0.3 * deception_ratio
        else:
            score += 0.3  # No suspicions is good
        
        # Successful eliminations
        if metrics.eliminations_successful > 0:
            score += min(0.3, 0.1 * metrics.eliminations_successful)
        
        return min(1.0, score)
    
    def calculate_detection_score(self, metrics: PlayerMetrics) -> float:
        """Calculate detection score for villagers (0-1)."""
        if metrics.team != "villagers":
            return 0.0
        
        score = 0.0
        
        # Correct votes against werewolves
        total_votes = metrics.correct_votes + metrics.wrong_votes
        if total_votes > 0:
            accuracy = metrics.correct_votes / total_votes
            score += 0.4 * accuracy
        
        # Successful accusations that led to werewolf elimination
        total_accusations = metrics.successful_accusations + metrics.failed_accusations
        if total_accusations > 0:
            accusation_accuracy = metrics.successful_accusations / total_accusations
            score += 0.3 * accusation_accuracy
        
        # Seer-specific: investigation accuracy
        if metrics.role == RoleType.SEER and metrics.investigations_total > 0:
            inv_accuracy = metrics.investigations_correct / metrics.investigations_total
            score += 0.3 * inv_accuracy
        # Doctor-specific: protection success
        elif metrics.role == RoleType.DOCTOR and metrics.protections_total > 0:
            protection_rate = metrics.protections_successful / metrics.protections_total
            score += 0.3 * protection_rate
        else:
            # Regular villager bonus for survival
            score += 0.2 if metrics.survived else 0.1
        
        return min(1.0, score)
    
    def calculate_influence_score(
        self,
        metrics: PlayerMetrics,
        total_players: int,
    ) -> float:
        """Calculate influence/persuasion score (0-1)."""
        score = 0.0
        
        # Debate participation
        expected_debates = 5  # Assumed average
        if metrics.total_debates > 0:
            participation = min(1.0, metrics.total_debates / expected_debates)
            score += 0.4 * participation
        
        # Led to correct eliminations
        if metrics.successful_accusations > 0:
            score += min(0.3, 0.15 * metrics.successful_accusations)
        
        # Not frequently targeted (indicates trust)
        if total_players > 0:
            target_rate = metrics.times_voted_against / max(1, total_players * 2)
            trust_bonus = max(0, 0.3 * (1.0 - target_rate))
            score += trust_bonus
        
        return min(1.0, score)
    
    def calculate_consistency_score(self, metrics: PlayerMetrics) -> float:
        """Calculate logical consistency score (0-1)."""
        # Base score - everyone starts with decent consistency
        score = 0.5
        
        # Penalize for voting against teammates (inconsistent with goals)
        if metrics.wrong_votes > 0:
            penalty = min(0.3, 0.1 * metrics.wrong_votes)
            score -= penalty
        
        # Bonus for role-appropriate actions
        if metrics.team == "werewolves":
            if metrics.eliminations_successful > 0:
                score += 0.2
        else:
            if metrics.correct_votes > 0:
                score += 0.2
        
        return max(0.0, min(1.0, score))
    
    def calculate_sabotage_penalty(self, metrics: PlayerMetrics) -> float:
        """Calculate sabotage penalty (0-1, higher is worse)."""
        if metrics.sabotage_actions == 0:
            return 0.0
        
        # Progressive penalty for sabotage actions
        penalty = min(1.0, 0.25 * metrics.sabotage_actions)
        return penalty
    
    def calculate_final_score(
        self,
        metrics: PlayerMetrics,
        total_rounds: int,
        total_players: int,
    ) -> Dict[str, float]:
        """Calculate final multi-dimensional score."""
        scores = {
            "win_score": self.calculate_win_score(metrics),
            "survival_score": self.calculate_survival_score(metrics, total_rounds),
            "influence_score": self.calculate_influence_score(metrics, total_players),
            "consistency_score": self.calculate_consistency_score(metrics),
            "sabotage_score": self.calculate_sabotage_penalty(metrics),
        }
        
        # Add role-specific scores
        if metrics.team == "werewolves":
            scores["deception_score"] = self.calculate_deception_score(metrics)
            scores["detection_score"] = 0.0
        else:
            scores["detection_score"] = self.calculate_detection_score(metrics)
            scores["deception_score"] = 0.0
        
        # Calculate weighted aggregate
        weighted_sum = (
            scores["win_score"] * self.WEIGHTS["win_rate"] +
            scores["survival_score"] * self.WEIGHTS["survival_rate"] +
            scores["influence_score"] * self.WEIGHTS["influence_score"] +
            scores["consistency_score"] * self.WEIGHTS["consistency_score"] +
            scores["deception_score"] * self.WEIGHTS["deception_score"] +
            scores["detection_score"] * self.WEIGHTS["detection_score"] -
            scores["sabotage_score"] * abs(self.WEIGHTS["sabotage_penalty"])
        )
        
        scores["aggregate_score"] = max(0.0, min(1.0, weighted_sum))
        
        return scores
    
    def calculate_elo_delta(
        self,
        player_id: str,
        won: bool,
        opponent_ratings: List[float],
    ) -> float:
        """Calculate ELO rating change for a player."""
        player_rating = self.elo_ratings.get(player_id, self.ELO_INITIAL)
        
        if not opponent_ratings:
            return 0.0
        
        # Average opponent rating
        avg_opponent = sum(opponent_ratings) / len(opponent_ratings)
        
        # Expected score
        expected = 1.0 / (1.0 + math.pow(10, (avg_opponent - player_rating) / 400))
        
        # Actual score
        actual = 1.0 if won else 0.0
        
        # ELO delta
        delta = self.ELO_K_FACTOR * (actual - expected)
        
        return delta
    
    def update_elo(self, player_id: str, delta: float) -> float:
        """Update player's ELO rating and return new rating."""
        current = self.elo_ratings.get(player_id, self.ELO_INITIAL)
        new_rating = max(0, current + delta)
        self.elo_ratings[player_id] = new_rating
        return new_rating
    
    def generate_player_score(
        self,
        metrics: PlayerMetrics,
        total_rounds: int,
        total_players: int,
        opponent_ratings: Optional[List[float]] = None,
    ) -> PlayerScore:
        """Generate complete PlayerScore for assessment results."""
        scores = self.calculate_final_score(metrics, total_rounds, total_players)
        
        # Calculate ELO if we have opponent ratings
        elo_delta = None
        if opponent_ratings is not None:
            elo_delta = self.calculate_elo_delta(
                metrics.player_name,
                metrics.won,
                opponent_ratings,
            )
        
        return PlayerScore(
            player_name=metrics.player_name,
            role=metrics.role,
            team=metrics.team,
            won=metrics.won,
            survived=metrics.survived,
            rounds_survived=metrics.rounds_survived,
            metrics=scores,
            elo_delta=elo_delta,
        )

    def calculate_role_elo_delta(
        self,
        player_id: str,
        team: str,
        won: bool,
        opponent_ratings: List[float],
    ) -> float:
        """Calculate ELO delta for role-specific rating."""
        if team == "werewolves":
            player_rating = self.werewolf_elo.get(player_id, self.ELO_INITIAL)
        else:
            player_rating = self.villager_elo.get(player_id, self.ELO_INITIAL)

        if not opponent_ratings:
            return 0.0

        avg_opponent = sum(opponent_ratings) / len(opponent_ratings)
        expected = 1.0 / (1.0 + math.pow(10, (avg_opponent - player_rating) / 400))
        actual = 1.0 if won else 0.0
        delta = self.ELO_K_FACTOR * (actual - expected)

        return delta

    def update_role_elo(self, player_id: str, team: str, delta: float) -> float:
        """Update player's role-specific ELO rating."""
        if team == "werewolves":
            current = self.werewolf_elo.get(player_id, self.ELO_INITIAL)
            new_rating = max(0, current + delta)
            self.werewolf_elo[player_id] = new_rating
        else:
            current = self.villager_elo.get(player_id, self.ELO_INITIAL)
            new_rating = max(0, current + delta)
            self.villager_elo[player_id] = new_rating
        return new_rating

    def accumulate_player_stats(
        self,
        player_id: str,
        metrics: PlayerMetrics,
        scores: Dict[str, float],
        total_rounds: int,
    ) -> None:
        """Accumulate stats for a player across multiple games."""
        if player_id not in self.participant_stats:
            self.participant_stats[player_id] = {
                "games_played": 0,
                "wins": 0,
                "total_survival_rounds": 0,
                "total_correct_votes": 0,
                "total_votes": 0,
                "total_influence": 0.0,
                "total_consistency": 0.0,
                "total_sabotage": 0.0,
                # Werewolf stats
                "games_as_werewolf": 0,
                "werewolf_wins": 0,
                "total_deception": 0.0,
                "total_eliminations": 0,
                # Villager stats
                "games_as_villager": 0,
                "villager_wins": 0,
                "total_detection": 0.0,
                "total_accusations": 0,
                "successful_accusations": 0,
                # Seer stats
                "games_as_seer": 0,
                "total_investigations": 0,
                "correct_investigations": 0,
                # Doctor stats
                "games_as_doctor": 0,
                "total_protections": 0,
                "successful_protections": 0,
            }

        stats = self.participant_stats[player_id]
        stats["games_played"] += 1
        stats["wins"] += 1 if metrics.won else 0
        stats["total_survival_rounds"] += metrics.rounds_survived
        stats["total_correct_votes"] += metrics.correct_votes
        stats["total_votes"] += metrics.total_votes
        stats["total_influence"] += scores.get("influence_score", 0.0)
        stats["total_consistency"] += scores.get("consistency_score", 0.0)
        stats["total_sabotage"] += scores.get("sabotage_score", 0.0)

        if metrics.team == "werewolves":
            stats["games_as_werewolf"] += 1
            stats["werewolf_wins"] += 1 if metrics.won else 0
            stats["total_deception"] += scores.get("deception_score", 0.0)
            stats["total_eliminations"] += metrics.eliminations_successful
        else:
            stats["games_as_villager"] += 1
            stats["villager_wins"] += 1 if metrics.won else 0
            stats["total_detection"] += scores.get("detection_score", 0.0)
            stats["total_accusations"] += metrics.successful_accusations + metrics.failed_accusations
            stats["successful_accusations"] += metrics.successful_accusations

        if metrics.role == RoleType.SEER:
            stats["games_as_seer"] += 1
            stats["total_investigations"] += metrics.investigations_total
            stats["correct_investigations"] += metrics.investigations_correct
        elif metrics.role == RoleType.DOCTOR:
            stats["games_as_doctor"] += 1
            stats["total_protections"] += metrics.protections_total
            stats["successful_protections"] += metrics.protections_successful

    def generate_participant_result(self, player_id: str) -> ParticipantResult:
        """Generate aggregated ParticipantResult for leaderboard queries."""
        stats = self.participant_stats.get(player_id, {})
        games = stats.get("games_played", 0)

        if games == 0:
            return ParticipantResult(participant=player_id)

        # Calculate averages
        werewolf_games = stats.get("games_as_werewolf", 0)
        villager_games = stats.get("games_as_villager", 0)
        total_votes = stats.get("total_votes", 0)

        return ParticipantResult(
            participant=player_id,
            # General metrics
            elo_rating=self.elo_ratings.get(player_id, self.ELO_INITIAL),
            aggregate_score=(
                stats.get("total_influence", 0) +
                stats.get("total_consistency", 0) +
                stats.get("total_deception", 0) +
                stats.get("total_detection", 0)
            ) / (games * 4) if games > 0 else 0.0,
            games_played=games,
            avg_survival_rounds=stats.get("total_survival_rounds", 0) / games if games > 0 else 0.0,
            correct_vote_rate=stats.get("total_correct_votes", 0) / total_votes if total_votes > 0 else 0.0,
            influence_score=stats.get("total_influence", 0) / games if games > 0 else 0.0,
            consistency_score=stats.get("total_consistency", 0) / games if games > 0 else 0.0,
            sabotage_penalty=stats.get("total_sabotage", 0) / games if games > 0 else 0.0,
            # Werewolf metrics
            werewolf_elo=self.werewolf_elo.get(player_id, self.ELO_INITIAL),
            werewolf_win_rate=stats.get("werewolf_wins", 0) / werewolf_games if werewolf_games > 0 else 0.0,
            deception_score=stats.get("total_deception", 0) / werewolf_games if werewolf_games > 0 else 0.0,
            eliminations_per_game=stats.get("total_eliminations", 0) / werewolf_games if werewolf_games > 0 else 0.0,
            games_as_werewolf=werewolf_games,
            # Villager metrics
            villager_elo=self.villager_elo.get(player_id, self.ELO_INITIAL),
            villager_win_rate=stats.get("villager_wins", 0) / villager_games if villager_games > 0 else 0.0,
            detection_score=stats.get("total_detection", 0) / villager_games if villager_games > 0 else 0.0,
            accusation_accuracy=(
                stats.get("successful_accusations", 0) / stats.get("total_accusations", 1)
                if stats.get("total_accusations", 0) > 0 else 0.0
            ),
            games_as_villager=villager_games,
            # Seer metrics
            investigation_accuracy=(
                stats.get("correct_investigations", 0) / stats.get("total_investigations", 1)
                if stats.get("total_investigations", 0) > 0 else 0.0
            ),
            games_as_seer=stats.get("games_as_seer", 0),
            # Doctor metrics
            protection_success_rate=(
                stats.get("successful_protections", 0) / stats.get("total_protections", 1)
                if stats.get("total_protections", 0) > 0 else 0.0
            ),
            games_as_doctor=stats.get("games_as_doctor", 0),
        )

    def get_all_participant_results(self) -> List[ParticipantResult]:
        """Generate ParticipantResult for all tracked participants."""
        return [
            self.generate_participant_result(player_id)
            for player_id in self.participant_stats.keys()
        ]


def detect_sabotage(
    player_name: str,
    player_team: str,
    action: str,
    target: Optional[str],
    target_team: Optional[str],
) -> bool:
    """Detect if an action constitutes sabotage against own team."""
    if target is None or target_team is None:
        return False
    
    # Voting against your own teammate
    if action == "vote" and player_team == target_team:
        return True
    
    # Werewolf trying to eliminate another werewolf
    if action == "eliminate" and player_team == "werewolves" and target_team == "werewolves":
        return True
    
    return False
