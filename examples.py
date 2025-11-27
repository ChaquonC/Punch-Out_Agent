#!/usr/bin/env python3
"""
Example: Using the Punch-Out AI

This script demonstrates how to use the AI controller with different configurations.
"""

import json
from python.punchout_ai import PunchOutAI, GameState, Move


def example_basic_usage():
    """Example 1: Basic AI usage"""
    print("=" * 60)
    print("Example 1: Basic AI Usage")
    print("=" * 60)
    
    # Create AI instance
    ai = PunchOutAI()
    
    # Create a game state
    state = GameState()
    state.player_health = 96
    state.player_stamina = 100
    state.player_stars = 0
    state.opponent_health = 100
    state.opponent_attack = 0
    state.frame_counter = 0
    
    # Get AI decision
    decision = ai.make_decision(state)
    print(f"Current State: {state.to_dict()}")
    print(f"AI Decision: {decision.value}\n")


def example_defensive_scenario():
    """Example 2: Defensive scenario - opponent attacking"""
    print("=" * 60)
    print("Example 2: Defensive Scenario (Opponent Attacking)")
    print("=" * 60)
    
    ai = PunchOutAI()
    
    # Simulate opponent left hook attack
    state = GameState()
    state.player_health = 50
    state.player_stamina = 80
    state.player_stars = 1
    state.opponent_health = 75
    state.opponent_attack = 5  # Left hook (1-10 range)
    state.frame_counter = 200
    
    decision = ai.make_decision(state)
    print(f"Opponent is throwing a LEFT HOOK!")
    print(f"Player Health: {state.player_health}")
    print(f"AI Decision: {decision.value}")
    print("Expected: DODGE_RIGHT\n")


def example_offensive_scenario():
    """Example 3: Offensive scenario - safe to attack"""
    print("=" * 60)
    print("Example 3: Offensive Scenario (Safe to Attack)")
    print("=" * 60)
    
    # Create aggressive AI
    config = {
        'reaction_time': 5,
        'aggression_level': 0.8,  # High aggression
        'learning_enabled': True,
    }
    
    ai = PunchOutAI()
    ai.config = config
    
    state = GameState()
    state.player_health = 96
    state.player_stamina = 100
    state.player_stars = 2
    state.opponent_health = 80
    state.opponent_attack = 0  # No attack
    state.frame_counter = 300
    
    decision = ai.make_decision(state)
    print(f"Opponent is IDLE - safe to attack!")
    print(f"Player Stars: {state.player_stars}")
    print(f"Aggression Level: {config['aggression_level']}")
    print(f"AI Decision: {decision.value}")
    print("Expected: Offensive move (star punch or hook)\n")


def example_low_stamina():
    """Example 4: Low stamina scenario"""
    print("=" * 60)
    print("Example 4: Low Stamina Scenario")
    print("=" * 60)
    
    ai = PunchOutAI()
    
    state = GameState()
    state.player_health = 80
    state.player_stamina = 20  # Very low
    state.player_stars = 0
    state.opponent_health = 90
    state.opponent_attack = 0
    state.frame_counter = 500
    
    decision = ai.make_decision(state)
    print(f"Player Stamina: {state.player_stamina} (LOW!)")
    print(f"AI Decision: {decision.value}")
    print("Expected: IDLE (resting to recover stamina)\n")


def example_pattern_learning():
    """Example 5: Pattern learning over time"""
    print("=" * 60)
    print("Example 5: Pattern Learning")
    print("=" * 60)
    
    ai = PunchOutAI()
    
    print("Simulating 10 frames of gameplay...")
    
    # Simulate a pattern of attacks
    for i in range(10):
        state = GameState()
        state.player_health = 90 - i
        state.player_stamina = 80
        state.player_stars = 0
        state.opponent_health = 100 - (i * 2)
        
        # Simulate alternating attack pattern
        if i % 3 == 0:
            state.opponent_attack = 5  # Left hook
        elif i % 3 == 1:
            state.opponent_attack = 15  # Right hook
        else:
            state.opponent_attack = 0  # Idle
        
        state.frame_counter = i * 10
        
        decision = ai.make_decision(state)
        print(f"Frame {i}: Attack={state.opponent_attack}, Decision={decision.value}")
    
    stats = ai.get_statistics()
    print(f"\nLearning Statistics: {stats}\n")


def example_custom_config():
    """Example 6: Using custom configuration file"""
    print("=" * 60)
    print("Example 6: Custom Configuration")
    print("=" * 60)
    
    # Load the config file
    config_path = 'config/game_config.json'
    
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"Loaded configuration from: {config_path}")
        print(f"AI Config: {json.dumps(config.get('ai_config', {}), indent=2)}")
        
        # Show opponent patterns
        print("\nKnown Opponents:")
        for opp_id, opp_name in config.get('opponents', {}).items():
            print(f"  {opp_id}: {opp_name}")
        
        print("\nSample Attack Pattern (Glass Joe):")
        glass_joe = config.get('attack_patterns', {}).get('Glass Joe', {})
        print(f"  Tells: {glass_joe.get('tells', [])}")
        print(f"  Vulnerabilities: {glass_joe.get('vulnerabilities', [])}\n")
        
    except FileNotFoundError:
        print(f"Config file not found: {config_path}")
        print("Make sure you're running from the project root directory.\n")


def main():
    """Run all examples"""
    print("\n")
    print("╔" + "=" * 58 + "╗")
    print("║" + " " * 10 + "Punch-Out AI Agent Examples" + " " * 20 + "║")
    print("╚" + "=" * 58 + "╝")
    print("\n")
    
    example_basic_usage()
    example_defensive_scenario()
    example_offensive_scenario()
    example_low_stamina()
    example_pattern_learning()
    example_custom_config()
    
    print("=" * 60)
    print("All examples completed!")
    print("=" * 60)


if __name__ == "__main__":
    main()
