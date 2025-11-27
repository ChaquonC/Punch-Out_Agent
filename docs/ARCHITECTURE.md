# Project Architecture

## Overview

This document explains the technical architecture of the Punch-Out AI Agent.

## System Components

### 1. Lua Interface Layer (`lua/punchout_agent.lua`)

**Purpose**: Direct integration with NES emulators

**Responsibilities**:
- Read NES memory addresses in real-time
- Detect game state changes
- Send controller inputs to emulator
- Provide on-screen debug visualization
- Execute basic rule-based AI logic

**APIs Used**:
- BizHawk: `memory.readbyte()`, `joypad.set()`, `gui.text()`, `emu.frameadvance()`
- FCEUX: `memory.readbyte()`, `emu.joypad()`, `emu.registerafter()`

**Key Functions**:
- `updateGameState()`: Reads all game memory into local state
- `executeMove()`: Translates AI decision into controller inputs
- `detectOpponentAttack()`: Identifies opponent attack patterns
- `makeDecision()`: Simple rule-based decision making
- `mainLoop()`: Main execution loop called every frame

### 2. Python AI Engine (`python/punchout_ai.py`)

**Purpose**: Advanced AI logic and pattern recognition

**Components**:

#### GameState Class
- Represents a snapshot of game state
- Parses CSV data from Lua script
- Converts to dictionary for analysis

#### PunchOutAI Class
- **Pattern Detection**: Analyzes opponent animations
- **State Tracking**: Maintains history of game states
- **Decision Making**: Chooses optimal moves based on situation
- **Learning**: Identifies patterns in opponent behavior
- **Configuration**: Adjustable parameters for AI behavior

**Decision Algorithm**:
1. Update state history
2. Detect current opponent attack
3. Predict future attacks based on patterns
4. Choose counter-move or offensive strategy
5. Record decision in move history

**Strategies**:
- **Defensive**: React to opponent attacks with dodges/blocks
- **Offensive**: Attack when safe, prioritize star punches
- **Adaptive**: Adjust based on stamina and health

### 3. Configuration Layer (`config/game_config.json`)

**Contains**:
- NES memory addresses for different game versions
- Opponent database (names and IDs)
- Attack pattern data for each opponent
- AI behavioral parameters
- Game timing and thresholds

**Customization Points**:
- `reaction_time_frames`: Response delay (5 frames default)
- `aggression_level`: 0.0 (defensive) to 1.0 (aggressive)
- `learning_enabled`: Enable/disable pattern learning
- `star_punch_priority`: Always use star punches when available

## Data Flow

### Standalone Lua Mode

```
┌─────────────────┐
│  NES Emulator   │
│  (BizHawk/FCEUX)│
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Lua Script     │
│  - Read Memory  │
│  - AI Logic     │
│  - Send Inputs  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Game Display   │
│  + Debug Info   │
└─────────────────┘
```

### Integrated Mode (Future Enhancement)

```
┌─────────────────┐
│  NES Emulator   │
└────────┬────────┘
         │ memory read
         ▼
┌─────────────────┐      ┌──────────────────┐
│  Lua Script     │◄────►│  Python AI       │
│  - Read Memory  │ IPC  │  - Pattern Learn │
│  - Send Inputs  │      │  - Strategy      │
└─────────────────┘      │  - Analytics     │
                         └──────────────────┘
```

## Memory Map

### Player Data (Little Mac)
- `0x0391`: Health (96 = full)
- `0x0392`: Stamina (0-255)
- `0x0019`: Star count (0-3)
- `0x0380`: Animation frame
- `0x0382/0x0383`: Position (X, Y)

### Opponent Data
- `0x0398`: Health
- `0x0070`: State (idle, attacking, stunned)
- `0x0031`: Opponent ID (0-10)
- `0x0390`: Animation frame
- `0x0072`: Attack type/phase
- `0x0396/0x0397`: Position (X, Y)

### Game State
- `0x0001`: Game mode (menu, fight, etc.)
- `0x0002`: Round number (1-3)
- `0x001A`: Frame counter
- `0x0030/0x0031`: Timer (minutes, seconds)

## AI Decision Matrix

| Situation | Opponent Action | AI Response |
|-----------|----------------|-------------|
| Normal | Left Hook | Dodge Right |
| Normal | Right Hook | Dodge Left |
| Normal | Uppercut | Duck |
| Normal | Jab | Block |
| Safe | Idle | Attack (Jab/Hook) |
| Stars Available | Idle | Star Punch |
| Low Stamina | Any | Rest (Idle) |
| Low Health | Attack | Defensive Priority |

## Performance Considerations

### Frame Timing
- NES runs at 60 FPS (~16.67ms per frame)
- Lua script executes once per frame
- Reaction time configurable (default 5 frames = ~83ms)
- Human average reaction: ~200ms (12 frames)

### Memory Efficiency
- State history limited to 100 frames
- Move history limited to 100 actions
- Pattern data stored per opponent (11 total)

### Optimization Strategies
- Use simple rule checks before complex analysis
- Cache frequently accessed memory values
- Limit pattern learning window size
- Disable debug rendering for speed

## Extension Points

### Adding New Opponents
1. Add opponent ID to config
2. Define attack patterns (tells, vulnerabilities)
3. Update pattern detection logic
4. Add specific counter strategies

### Machine Learning Integration
1. Collect training data (states + outcomes)
2. Train model on successful sequences
3. Replace rule-based decision with ML predictions
4. Implement Q-learning or policy gradients

### Advanced Features
- Save state analysis for training
- Replay analysis and optimization
- Multi-opponent strategy switching
- Perfect frame timing for TAS-level play
- Video analysis for visual pattern detection

## Testing Strategy

### Unit Tests (`python/test_punchout_ai.py`)
- GameState parsing and serialization
- Attack detection accuracy
- Counter-move selection
- State history management
- Statistical tracking

### Integration Tests (Manual)
1. Load ROM in emulator
2. Run Lua script
3. Observe AI behavior against each opponent
4. Verify counter-moves execute correctly
5. Check debug output matches game state

### Performance Tests
- Frame rate stability
- Memory usage over time
- Decision latency measurements
- Pattern learning effectiveness

## Known Limitations

1. **Memory Addresses**: May vary between ROM versions
2. **Emulator Compatibility**: Tested on BizHawk/FCEUX only
3. **Pattern Recognition**: Limited to animation-based detection
4. **Learning**: Basic pattern matching, no ML currently
5. **Timing**: Frame-perfect execution not guaranteed

## Future Improvements

1. **Socket Communication**: Lua ↔ Python real-time integration
2. **Machine Learning**: Neural network for decision making
3. **Visual Analysis**: Screen capture for pattern detection
4. **Training Mode**: Automated data collection
5. **Tournament System**: Multi-fight analysis
6. **Speedrun Optimization**: TAS-level precise timing

## References

- [NES CPU Memory Map](https://wiki.nesdev.com/w/index.php/CPU_memory_map)
- [BizHawk Lua API](http://tasvideos.org/Bizhawk/LuaFunctions.html)
- [FCEUX Lua Reference](http://fceux.com/web/help/fceux.html?LuaScripting.html)
- [Punch-Out Game Mechanics](https://punchout.fandom.com/wiki/Mike_Tyson%27s_Punch-Out!!)
