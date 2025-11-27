# Quick Start Guide

Get the Punch-Out AI Agent running in 5 minutes!

## Prerequisites

✅ NES emulator (BizHawk recommended)  
✅ Mike Tyson's Punch-Out!! ROM (legally obtained)  
✅ Python 3.7+ (optional, for advanced features)

## Step-by-Step Setup

### 1. Download BizHawk Emulator

**Windows:**
```bash
# Download from https://tasvideos.org/BizHawk/ReleaseHistory
# Extract to C:\BizHawk
# Run EmuHawk.exe
```

**Linux:**
```bash
sudo apt install mono-complete
# Download BizHawk Linux build
mono EmuHawk.exe
```

### 2. Clone This Repository

```bash
git clone https://github.com/ChaquonC/Punch-Out_Agent.git
cd Punch-Out_Agent
```

### 3. Load the Game

1. Open BizHawk
2. File → Open ROM
3. Select your Punch-Out!! ROM
4. Game should start

### 4. Load the AI Script

1. In BizHawk: Tools → Lua Console
2. Click "Open Script"
3. Navigate to `lua/punchout_agent.lua`
4. Click "Open"

### 5. Watch the AI Play!

The AI will immediately start controlling Little Mac:
- Debug info appears on screen
- AI decisions shown in real-time
- Automatic dodge/attack behavior

## Optional: Python Setup

For advanced AI features:

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Test the AI
python examples.py
```

## Quick Configuration

Edit `config/game_config.json` to customize:

```json
{
  "ai_config": {
    "reaction_time_frames": 5,     // Lower = faster
    "aggression_level": 0.5,       // 0.0 to 1.0
    "star_punch_priority": true    // Use stars ASAP
  }
}
```

## Troubleshooting

**Problem: Script won't load**
- Solution: Make sure you're using BizHawk 2.8+ or FCEUX 2.6+

**Problem: AI doesn't respond**
- Solution: Check that ROM is Mike Tyson's Punch-Out!! (not Mr. Dream version)

**Problem: Game crashes**
- Solution: Try reducing emulator speed or disabling debug display

## Next Steps

📖 Read [SETUP.md](SETUP.md) for detailed configuration  
🏗️ Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical details  
🧪 Run `python python/test_punchout_ai.py` for unit tests  
🎮 Experiment with different AI strategies!

## Tips for Best Results

1. **Start with Glass Joe** - Easiest opponent, good for testing
2. **Adjust reaction time** - Lower values = faster AI responses
3. **Watch the debug output** - Learn what the AI is "thinking"
4. **Try different aggression levels** - See how behavior changes
5. **Save states** - Use emulator save states to practice specific situations

## Common Controls

- **Emulator Speed**: Alt + Plus/Minus
- **Pause**: Pause/Break key
- **Save State**: Shift + F1-F10
- **Load State**: F1-F10
- **Reset**: Ctrl + R

## Performance Tips

For smooth 60 FPS:
- Disable video filters in emulator
- Lower screen resolution
- Close unnecessary programs
- Comment out debug rendering in Lua script

## Have Fun!

This is a research project exploring classic AI techniques. Experiment, modify, and share your improvements!

---

**Need Help?** Open an issue on GitHub  
**Found a Bug?** Submit a pull request  
**Made Improvements?** We'd love to see them!
