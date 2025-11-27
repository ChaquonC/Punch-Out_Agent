# Punch-Out AI Agent

A classic artificial intelligence agent for playing Mike Tyson's Punch-Out!! on the NES. This project combines Lua scripting for emulator integration with Python for advanced AI decision-making.

## Overview

This AI agent can:
- Read game memory in real-time from NES emulators
- Detect opponent attack patterns and animations
- Make strategic decisions for dodging, blocking, and counter-attacking
- Control Little Mac through automated inputs
- Learn opponent patterns over time

## Project Structure

```
Punch-Out_Agent/
├── lua/
│   └── punchout_agent.lua      # Lua script for emulator interface
├── python/
│   └── punchout_ai.py          # Python AI controller
├── config/
│   └── game_config.json        # Game memory addresses and patterns
├── docs/
│   └── SETUP.md                # Detailed setup instructions
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features

### Lua Script (`lua/punchout_agent.lua`)
- **Memory Reading**: Reads game state from NES memory
- **Input Control**: Sends controller inputs to the emulator
- **Pattern Detection**: Identifies opponent attack animations
- **Built-in AI**: Simple rule-based decision making
- **Debug Display**: On-screen display of game state

### Python Script (`python/punchout_ai.py`)
- **Advanced AI**: More sophisticated decision-making algorithms
- **Pattern Learning**: Learns opponent patterns from history
- **State Tracking**: Maintains game state history
- **Statistics**: Tracks AI performance metrics
- **Configurable**: Adjustable aggression and reaction time

## Quick Start

### Prerequisites

1. **NES Emulator** (one of the following):
   - [BizHawk](http://tasvideos.org/BizHawk.html) (recommended)
   - [FCEUX](http://fceux.com/)

2. **Mike Tyson's Punch-Out!! ROM** (legally obtained)

3. **Python 3.7+** (for advanced AI features)

### Installation

1. Clone this repository:
```bash
git clone https://github.com/ChaquonC/Punch-Out_Agent.git
cd Punch-Out_Agent
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

### Usage with BizHawk

1. Open BizHawk emulator
2. Load Mike Tyson's Punch-Out!! ROM
3. Go to `Tools` → `Lua Console`
4. Click `Open Script` and select `lua/punchout_agent.lua`
5. The AI will start controlling Little Mac automatically

### Usage with FCEUX

1. Open FCEUX emulator
2. Load Mike Tyson's Punch-Out!! ROM
3. Go to `File` → `Lua` → `New Lua Script Window`
4. Browse and select `lua/punchout_agent.lua`
5. The AI will start playing

### Using the Python AI

The Python script can be used standalone for testing AI logic:

```bash
python python/punchout_ai.py
```

For integration with the Lua script, you would need to set up inter-process communication (see Advanced Usage).

## Configuration

Edit `config/game_config.json` to customize:

- **AI Behavior**:
  - `reaction_time_frames`: How many frames delay before reacting (lower = faster)
  - `aggression_level`: 0.0 (defensive) to 1.0 (aggressive)
  - `learning_enabled`: Enable pattern learning

- **Game Parameters**:
  - Memory addresses for different game versions
  - Opponent-specific attack patterns
  - Known tells and vulnerabilities

## AI Strategies

### Rule-Based (Lua)
- Detect opponent attack from animation state
- Execute pre-programmed counter moves
- Basic offensive patterns during safe moments

### Advanced (Python)
- Pattern recognition from state history
- Predictive attack detection
- Adaptive strategy based on opponent
- Statistical decision making

## Known Opponents

The AI has pattern data for:
1. Glass Joe
2. Von Kaiser
3. Piston Honda
4. Don Flamenco
5. King Hippo
6. Great Tiger
7. Bald Bull
8. Soda Popinski
9. Mr. Sandman
10. Super Macho Man
11. Mike Tyson

## Development

### Running Tests

```bash
pytest python/
```

### Code Quality

```bash
pylint python/punchout_ai.py
```

## Contributing

Contributions are welcome! Areas for improvement:
- More sophisticated machine learning models
- Better pattern recognition algorithms
- Support for additional emulators
- Training data collection and analysis
- Frame-perfect timing optimization

## Research Notes

This project explores classic AI techniques including:
- Finite state machines
- Rule-based expert systems
- Pattern matching and recognition
- Reactive planning
- Heuristic search

## License

See LICENSE file for details.

## Acknowledgments

- Mike Tyson's Punch-Out!! by Nintendo
- BizHawk and FCEUX emulator developers
- TASVideos community for game mechanics research

## References

- [Punch-Out!! Wiki](https://punchout.fandom.com/)
- [NES Dev Wiki](https://wiki.nesdev.com/)
- [TASVideos Resources](http://tasvideos.org/)

## Disclaimer

This project is for educational and research purposes. You must own a legal copy of Mike Tyson's Punch-Out!! to use this software.
