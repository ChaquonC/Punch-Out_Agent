#!/usr/bin/env python3
"""
Unit tests for Punch-Out AI Agent
"""

import sys
import os

# Add python directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__))))

from punchout_ai import PunchOutAI, GameState, Move, OpponentAttack


def test_game_state_creation():
    """Test GameState initialization"""
    state = GameState()
    assert state.player_health == 0
    assert state.player_stamina == 0
    assert state.opponent_health == 0
    print("✓ test_game_state_creation passed")


def test_game_state_from_string():
    """Test parsing GameState from CSV string"""
    state = GameState()
    state.from_string("96,80,1,100,0,5,15,100")
    
    assert state.player_health == 96
    assert state.player_stamina == 80
    assert state.player_stars == 1
    assert state.opponent_health == 100
    assert state.opponent_attack == 15
    print("✓ test_game_state_from_string passed")


def test_ai_creation():
    """Test AI initialization"""
    ai = PunchOutAI()
    assert ai is not None
    assert ai.config is not None
    print("✓ test_ai_creation passed")


def test_detect_left_hook():
    """Test detection of left hook attack"""
    ai = PunchOutAI()
    state = GameState()
    state.opponent_attack = 5  # In range 1-10 (left hook)
    
    attack = ai.detect_opponent_attack(state)
    assert attack == OpponentAttack.LEFT_HOOK
    print("✓ test_detect_left_hook passed")


def test_detect_right_hook():
    """Test detection of right hook attack"""
    ai = PunchOutAI()
    state = GameState()
    state.opponent_attack = 15  # In range 11-20 (right hook)
    
    attack = ai.detect_opponent_attack(state)
    assert attack == OpponentAttack.RIGHT_HOOK
    print("✓ test_detect_right_hook passed")


def test_counter_left_hook():
    """Test countering left hook with dodge right"""
    ai = PunchOutAI()
    state = GameState()
    state.player_health = 96
    state.player_stamina = 80
    state.opponent_attack = 5  # Left hook
    
    decision = ai.make_decision(state)
    assert decision == Move.DODGE_RIGHT
    print("✓ test_counter_left_hook passed")


def test_counter_right_hook():
    """Test countering right hook with dodge left"""
    ai = PunchOutAI()
    state = GameState()
    state.player_health = 96
    state.player_stamina = 80
    state.opponent_attack = 15  # Right hook
    
    decision = ai.make_decision(state)
    assert decision == Move.DODGE_LEFT
    print("✓ test_counter_right_hook passed")


def test_low_stamina_rest():
    """Test that AI rests when stamina is low"""
    ai = PunchOutAI()
    state = GameState()
    state.player_health = 96
    state.player_stamina = 20  # Very low
    state.opponent_attack = 0
    
    decision = ai.make_decision(state)
    assert decision == Move.IDLE
    print("✓ test_low_stamina_rest passed")


def test_star_punch_priority():
    """Test that AI prioritizes star punch when available"""
    ai = PunchOutAI()
    state = GameState()
    state.player_health = 96
    state.player_stamina = 100
    state.player_stars = 1  # Has stars
    state.opponent_health = 100
    state.opponent_attack = 0
    
    decision = ai.make_decision(state)
    assert decision == Move.STAR_PUNCH
    print("✓ test_star_punch_priority passed")


def test_state_history_tracking():
    """Test that AI tracks state history"""
    ai = PunchOutAI()
    state1 = GameState()
    state2 = GameState()
    
    ai.make_decision(state1)
    ai.make_decision(state2)
    
    assert len(ai.state_history) == 2
    print("✓ test_state_history_tracking passed")


def test_statistics():
    """Test AI statistics tracking"""
    ai = PunchOutAI()
    state = GameState()
    
    ai.make_decision(state)
    ai.make_decision(state)
    ai.make_decision(state)
    
    stats = ai.get_statistics()
    assert stats['states_processed'] == 3
    assert stats['moves_made'] == 3
    print("✓ test_statistics passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("Running Punch-Out AI Unit Tests")
    print("=" * 60 + "\n")
    
    tests = [
        test_game_state_creation,
        test_game_state_from_string,
        test_ai_creation,
        test_detect_left_hook,
        test_detect_right_hook,
        test_counter_left_hook,
        test_counter_right_hook,
        test_low_stamina_rest,
        test_star_punch_priority,
        test_state_history_tracking,
        test_statistics,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
        except Exception as e:
            print(f"✗ {test.__name__} error: {e}")
            failed += 1
    
    print("\n" + "=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60 + "\n")
    
    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
