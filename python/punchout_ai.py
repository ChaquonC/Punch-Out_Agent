#!/usr/bin/env python3
"""
Punch-Out AI Agent - Python Controller
This script implements a more sophisticated AI for controlling Little Mac
using machine learning or advanced heuristics.
"""

import time
import json
import os
from enum import Enum
from typing import Dict, List, Optional, Tuple


class Move(Enum):
    """Available moves for Little Mac"""
    IDLE = "IDLE"
    DODGE_LEFT = "DODGE_LEFT"
    DODGE_RIGHT = "DODGE_RIGHT"
    BLOCK = "BLOCK"
    DUCK = "DUCK"
    JAB_LEFT = "JAB_LEFT"
    JAB_RIGHT = "JAB_RIGHT"
    HOOK_LEFT = "HOOK_LEFT"
    HOOK_RIGHT = "HOOK_RIGHT"
    UPPERCUT = "UPPERCUT"
    STAR_PUNCH = "STAR_PUNCH"


class OpponentAttack(Enum):
    """Opponent attack patterns"""
    NONE = "NONE"
    LEFT_HOOK = "LEFT_HOOK"
    RIGHT_HOOK = "RIGHT_HOOK"
    UPPERCUT = "UPPERCUT"
    JAB = "JAB"


class GameState:
    """Represents the current state of the game"""
    
    def __init__(self):
        self.player_health: int = 0
        self.player_stamina: int = 0
        self.player_stars: int = 0
        self.opponent_health: int = 0
        self.opponent_state: int = 0
        self.opponent_anim: int = 0
        self.opponent_attack: int = 0
        self.frame_counter: int = 0
    
    def from_string(self, state_str: str) -> None:
        """Parse game state from CSV string"""
        parts = state_str.strip().split(',')
        if len(parts) >= 8:
            self.player_health = int(parts[0])
            self.player_stamina = int(parts[1])
            self.player_stars = int(parts[2])
            self.opponent_health = int(parts[3])
            self.opponent_state = int(parts[4])
            self.opponent_anim = int(parts[5])
            self.opponent_attack = int(parts[6])
            self.frame_counter = int(parts[7])
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        return {
            'player_health': self.player_health,
            'player_stamina': self.player_stamina,
            'player_stars': self.player_stars,
            'opponent_health': self.opponent_health,
            'opponent_state': self.opponent_state,
            'opponent_anim': self.opponent_anim,
            'opponent_attack': self.opponent_attack,
            'frame_counter': self.frame_counter,
        }


class PunchOutAI:
    """Main AI controller for Punch-Out"""
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.state_history: List[GameState] = []
        self.move_history: List[Move] = []
        self.opponent_patterns: Dict[int, List[OpponentAttack]] = {}
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration file"""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return {
            'reaction_time': 5,  # frames
            'aggression_level': 0.5,
            'learning_enabled': True,
        }
    
    def detect_opponent_attack(self, state: GameState) -> OpponentAttack:
        """Detect what attack the opponent is performing"""
        attack = state.opponent_attack
        
        if 1 <= attack <= 10:
            return OpponentAttack.LEFT_HOOK
        elif 11 <= attack <= 20:
            return OpponentAttack.RIGHT_HOOK
        elif 21 <= attack <= 30:
            return OpponentAttack.UPPERCUT
        elif 31 <= attack <= 40:
            return OpponentAttack.JAB
        else:
            return OpponentAttack.NONE
    
    def predict_next_attack(self, state: GameState) -> Optional[OpponentAttack]:
        """Predict opponent's next attack based on patterns"""
        # Simple pattern matching: look at recent history
        if len(self.state_history) < 10:
            return None
        
        # Check if opponent is winding up for an attack
        recent_states = self.state_history[-10:]
        anim_changes = [s.opponent_anim for s in recent_states]
        
        # Look for animation sequences that precede attacks
        # This would be enhanced with actual pattern data
        if len(set(anim_changes[-5:])) > 3:
            # Rapid animation changes suggest incoming attack
            return OpponentAttack.JAB
        
        return None
    
    def calculate_counter_move(self, attack: OpponentAttack, state: GameState) -> Move:
        """Calculate the best counter move for an opponent attack"""
        # Defensive responses
        counters = {
            OpponentAttack.LEFT_HOOK: Move.DODGE_RIGHT,
            OpponentAttack.RIGHT_HOOK: Move.DODGE_LEFT,
            OpponentAttack.UPPERCUT: Move.DUCK,
            OpponentAttack.JAB: Move.BLOCK,
            OpponentAttack.NONE: Move.IDLE,
        }
        
        base_counter = counters.get(attack, Move.IDLE)
        
        # Check if we can counter-attack instead
        if state.player_stamina > 60 and attack == OpponentAttack.NONE:
            # Use star punch if available
            if state.player_stars > 0:
                return Move.STAR_PUNCH
            # Otherwise throw hooks for damage
            if state.frame_counter % 40 < 20:
                return Move.HOOK_LEFT
            else:
                return Move.HOOK_RIGHT
        
        return base_counter
    
    def make_decision(self, state: GameState) -> Move:
        """Main decision-making function"""
        # Store state history for pattern learning
        self.state_history.append(state)
        if len(self.state_history) > 100:
            self.state_history.pop(0)
        
        # Detect current attack
        current_attack = self.detect_opponent_attack(state)
        
        # Predict future attack
        predicted_attack = self.predict_next_attack(state)
        
        # Make decision based on current situation
        if current_attack != OpponentAttack.NONE:
            # React to current attack
            move = self.calculate_counter_move(current_attack, state)
        elif predicted_attack is not None:
            # Pre-emptively react to predicted attack
            move = self.calculate_counter_move(predicted_attack, state)
        else:
            # Offensive strategy when safe
            move = self._offensive_strategy(state)
        
        # Store move history
        self.move_history.append(move)
        if len(self.move_history) > 100:
            self.move_history.pop(0)
        
        return move
    
    def _offensive_strategy(self, state: GameState) -> Move:
        """Determine offensive move when safe to attack"""
        if state.player_stamina < 30:
            # Too tired, rest
            return Move.IDLE
        
        if state.opponent_health <= 0:
            # Opponent down, no need to attack
            return Move.IDLE
        
        # Check if star punch should be prioritized
        star_punch_priority = self.config.get('star_punch_priority', True)
        if star_punch_priority and state.player_stars > 0:
            return Move.STAR_PUNCH
        
        # Aggressive configuration
        aggression = self.config.get('aggression_level', 0.5)
        
        if aggression > 0.7:
            # High aggression: use hooks and uppercuts
            if state.frame_counter % 60 < 20:
                return Move.HOOK_LEFT
            elif state.frame_counter % 60 < 40:
                return Move.HOOK_RIGHT
            else:
                return Move.UPPERCUT
        else:
            # Normal aggression: use jabs
            if state.frame_counter % 40 < 20:
                return Move.JAB_LEFT
            else:
                return Move.JAB_RIGHT
    
    def get_statistics(self) -> Dict:
        """Get AI performance statistics"""
        return {
            'states_processed': len(self.state_history),
            'moves_made': len(self.move_history),
            'patterns_learned': len(self.opponent_patterns),
        }


def main():
    """Main entry point for testing"""
    print("Punch-Out AI Agent (Python Controller)")
    print("=" * 50)
    
    # Initialize AI
    ai = PunchOutAI()
    
    # Simulate some game states for testing
    test_state = GameState()
    test_state.player_health = 96
    test_state.player_stamina = 80
    test_state.player_stars = 1
    test_state.opponent_health = 100
    test_state.opponent_attack = 15  # Right hook
    test_state.frame_counter = 100
    
    # Make decision
    decision = ai.make_decision(test_state)
    print(f"\nTest State: {test_state.to_dict()}")
    print(f"AI Decision: {decision.value}")
    
    # Show statistics
    stats = ai.get_statistics()
    print(f"\nStatistics: {stats}")


if __name__ == "__main__":
    main()
