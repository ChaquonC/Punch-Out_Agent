# Detailed Setup Guide

This guide provides step-by-step instructions for setting up and running the Punch-Out AI Agent.

## Table of Contents
1. [System Requirements](#system-requirements)
2. [Installing Emulators](#installing-emulators)
3. [Setting Up Python Environment](#setting-up-python-environment)
4. [Running the AI Agent](#running-the-ai-agent)
5. [Troubleshooting](#troubleshooting)
6. [Advanced Configuration](#advanced-configuration)

## System Requirements

### Minimum Requirements
- **OS**: Windows 10/11, macOS 10.14+, or Linux (Ubuntu 18.04+)
- **CPU**: Dual-core 2.0 GHz or better
- **RAM**: 2 GB
- **Storage**: 100 MB free space
- **Python**: 3.7 or higher

### Recommended Requirements
- **CPU**: Quad-core 2.5 GHz or better
- **RAM**: 4 GB
- **Python**: 3.9 or higher

## Installing Emulators

### Option 1: BizHawk (Recommended)

BizHawk is recommended for its superior Lua scripting capabilities and accuracy.

#### Windows
1. Download BizHawk from https://tasvideos.org/BizHawk/ReleaseHistory
2. Extract the ZIP file to a folder (e.g., `C:\BizHawk`)
3. Run `EmuHawk.exe`
4. On first run, it will download required components

#### Linux
1. Install Mono: `sudo apt install mono-complete`
2. Download BizHawk Linux build
3. Extract and run: `mono EmuHawk.exe`

#### macOS
BizHawk is not officially supported on macOS. Use FCEUX instead.

### Option 2: FCEUX

FCEUX is a good alternative with cross-platform support.

#### Windows
1. Download from http://fceux.com/web/download.html
2. Run the installer
3. Launch FCEUX

#### macOS
1. Install via Homebrew: `brew install fceux`
2. Or download from http://fceux.com/

#### Linux
1. Install via package manager: `sudo apt install fceux`
2. Or compile from source

## Setting Up Python Environment

### Step 1: Install Python

Check if Python is already installed:
```bash
python --version
```

If not installed, download from https://www.python.org/downloads/

### Step 2: Create Virtual Environment (Recommended)

```bash
# Navigate to project directory
cd Punch-Out_Agent

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Verify Installation

```bash
python python/punchout_ai.py
```

You should see the test output with AI statistics.

## Running the AI Agent

### Using BizHawk

1. **Launch BizHawk**
   ```bash
   # Navigate to BizHawk directory and run
   ./EmuHawk.exe
   ```

2. **Load the ROM**
   - File → Open ROM
   - Navigate to your Punch-Out!! ROM file
   - Click Open

3. **Load the Lua Script**
   - Tools → Lua Console
   - In the Lua Console window, click "Open Script"
   - Navigate to `lua/punchout_agent.lua`
   - Click Open

4. **Start Playing**
   - The AI will automatically start controlling the game
   - Debug information will appear on screen
   - You can pause/resume by pausing the emulator

### Using FCEUX

1. **Launch FCEUX**

2. **Load the ROM**
   - File → Open ROM
   - Select your Punch-Out!! ROM

3. **Load the Lua Script**
   - File → Lua → New Lua Script Window
   - Click "Browse"
   - Select `lua/punchout_agent.lua`
   - Click "Run"

4. **Monitor Progress**
   - The AI will control the game
   - Watch the debug output in the Lua console

### Testing Python AI Standalone

Run the Python AI independently to test decision-making:

```bash
python python/punchout_ai.py
```

This will run a simulation and display AI decisions.

## Troubleshooting

### Common Issues

#### Issue: "Script error: attempt to index global 'memory'"

**Solution**: The emulator might not support the memory API. Try using a different emulator version or check the Lua API documentation.

#### Issue: Python module not found

**Solution**: Ensure virtual environment is activated and dependencies are installed:
```bash
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

#### Issue: AI not responding to opponent attacks

**Solution**: 
1. Check that memory addresses in `config/game_config.json` match your ROM version
2. Verify the ROM is Mike Tyson's Punch-Out!! (not Punch-Out!! Featuring Mr. Dream)
3. Adjust `reaction_time_frames` in config to increase response speed

#### Issue: Game runs too fast/slow

**Solution**: Adjust emulator speed settings (usually under Config → Speed)

### Debug Mode

Enable additional debug output by modifying the Lua script:

1. Open `lua/punchout_agent.lua`
2. Find the `mainLoop()` function
3. Uncomment debug print statements

### Memory Address Verification

To verify memory addresses are correct:

1. Use the emulator's memory viewer/debugger
2. Compare values with known game states
3. Update `config/game_config.json` if addresses differ

## Advanced Configuration

### Customizing AI Behavior

Edit `config/game_config.json`:

```json
{
  "ai_config": {
    "reaction_time_frames": 5,        // Lower = faster reactions
    "aggression_level": 0.5,          // 0.0 = defensive, 1.0 = aggressive
    "learning_enabled": true,         // Enable pattern learning
    "defensive_mode_health_threshold": 50,  // Switch to defensive when low HP
    "stamina_conservation_threshold": 30,   // Rest when stamina is low
    "star_punch_priority": true,      // Prioritize using star punches
    "pattern_learning_window": 100    // Number of frames to analyze
  }
}
```

### Creating Opponent-Specific Strategies

Add custom patterns for specific opponents in the config file:

```json
{
  "attack_patterns": {
    "Custom Opponent": {
      "tells": [
        "Visual cue before attack",
        "Animation pattern"
      ],
      "vulnerabilities": [
        "Counter strategy 1",
        "Counter strategy 2"
      ]
    }
  }
}
```

### Integrating Python AI with Lua

For advanced users who want to use Python AI with the emulator:

1. Set up a socket server in Python
2. Modify Lua script to send game state to Python
3. Receive AI decisions from Python
4. Execute decisions in emulator

Example architecture:
```
Emulator (Lua) <--> Socket Communication <--> Python AI
```

This requires additional development and is not included in the base package.

### Performance Tuning

#### For Faster Execution:
- Reduce `pattern_learning_window` in config
- Disable on-screen debug display in Lua script
- Lower emulator video quality settings

#### For Better Accuracy:
- Increase `pattern_learning_window`
- Decrease `reaction_time_frames` (if your system can handle it)
- Enable save state management for training

## Next Steps

- Experiment with different aggression levels
- Try different opponents and observe AI behavior
- Modify attack patterns for specific opponents
- Contribute improvements back to the project

## Getting Help

- Check the [main README](../README.md) for general information
- Review code comments in Lua and Python files
- Open an issue on GitHub for bugs or questions

## References

- [BizHawk Documentation](http://tasvideos.org/BizHawk.html)
- [FCEUX Lua Reference](http://fceux.com/web/help/fceux.html?LuaScripting.html)
- [Punch-Out!! Game Mechanics](https://punchout.fandom.com/)
