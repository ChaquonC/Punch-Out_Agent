-- Punch-Out AI Agent - Lua Interface Script
-- Compatible with BizHawk and FCEUX emulators
-- This script reads game memory and sends inputs to the emulator

-- Memory addresses for Mike Tyson's Punch-Out!! (NES)
local MEMORY = {
    -- Player data
    PLAYER_HEALTH = 0x0391,
    PLAYER_STAMINA = 0x0392,
    PLAYER_STARS = 0x0019,
    
    -- Opponent data
    OPPONENT_HEALTH = 0x0398,
    OPPONENT_STATE = 0x0070,
    OPPONENT_ID = 0x0031,
    
    -- Game state
    GAME_MODE = 0x0001,
    ROUND_NUMBER = 0x0002,
    FRAME_COUNTER = 0x001A,
    
    -- Position and animation
    PLAYER_ANIM = 0x0380,
    OPPONENT_ANIM = 0x0390,
    OPPONENT_ATTACK = 0x0072,
}

-- Input buttons for controller
local BUTTONS = {
    A = "A",
    B = "B",
    UP = "Up",
    DOWN = "Down",
    LEFT = "Left",
    RIGHT = "Right",
    START = "Start",
    SELECT = "Select",
}

-- Game state tracker
local gameState = {
    playerHealth = 0,
    playerStamina = 0,
    playerStars = 0,
    opponentHealth = 0,
    opponentState = 0,
    opponentId = 0,
    gameMode = 0,
    roundNumber = 0,
    frameCounter = 0,
    playerAnim = 0,
    opponentAnim = 0,
    opponentAttack = 0,
}

-- Read a byte from memory
local function readByte(address)
    if memory then
        return memory.readbyte(address)
    elseif emu then
        return emu.read(address, emu.memType.cpuDebug)
    else
        return 0
    end
end

-- Update game state from memory
function updateGameState()
    gameState.playerHealth = readByte(MEMORY.PLAYER_HEALTH)
    gameState.playerStamina = readByte(MEMORY.PLAYER_STAMINA)
    gameState.playerStars = readByte(MEMORY.PLAYER_STARS)
    gameState.opponentHealth = readByte(MEMORY.OPPONENT_HEALTH)
    gameState.opponentState = readByte(MEMORY.OPPONENT_STATE)
    gameState.opponentId = readByte(MEMORY.OPPONENT_ID)
    gameState.gameMode = readByte(MEMORY.GAME_MODE)
    gameState.roundNumber = readByte(MEMORY.ROUND_NUMBER)
    gameState.frameCounter = readByte(MEMORY.FRAME_COUNTER)
    gameState.playerAnim = readByte(MEMORY.PLAYER_ANIM)
    gameState.opponentAnim = readByte(MEMORY.OPPONENT_ANIM)
    gameState.opponentAttack = readByte(MEMORY.OPPONENT_ATTACK)
end

-- Press a button (emulator-specific)
function pressButton(button)
    if joypad then
        local input = {}
        input[button] = true
        joypad.set(input)
    elseif emu then
        -- FCEUX style
        emu.joypad(1, {[button] = 1})
    end
end

-- Release all buttons
function releaseButtons()
    if joypad then
        joypad.set({})
    elseif emu then
        emu.joypad(1, {})
    end
end

-- Execute a move based on AI decision
function executeMove(move)
    if move == "DODGE_LEFT" then
        pressButton(BUTTONS.LEFT)
    elseif move == "DODGE_RIGHT" then
        pressButton(BUTTONS.RIGHT)
    elseif move == "BLOCK" then
        -- Block is typically no input or specific timing
        releaseButtons()
    elseif move == "DUCK" then
        pressButton(BUTTONS.DOWN)
    elseif move == "JAB_LEFT" then
        pressButton(BUTTONS.LEFT)
        pressButton(BUTTONS.A)
    elseif move == "JAB_RIGHT" then
        pressButton(BUTTONS.RIGHT)
        pressButton(BUTTONS.A)
    elseif move == "HOOK_LEFT" then
        pressButton(BUTTONS.LEFT)
        pressButton(BUTTONS.B)
    elseif move == "HOOK_RIGHT" then
        pressButton(BUTTONS.RIGHT)
        pressButton(BUTTONS.B)
    elseif move == "UPPERCUT" then
        pressButton(BUTTONS.UP)
        pressButton(BUTTONS.A)
    elseif move == "STAR_PUNCH" then
        pressButton(BUTTONS.START)
    else
        releaseButtons()
    end
end

-- Simple pattern recognition for opponent attacks
function detectOpponentAttack()
    -- Returns attack type based on opponent animation state
    local attack = gameState.opponentAttack
    
    if attack >= 1 and attack <= 10 then
        return "LEFT_HOOK"
    elseif attack >= 11 and attack <= 20 then
        return "RIGHT_HOOK"
    elseif attack >= 21 and attack <= 30 then
        return "UPPERCUT"
    elseif attack >= 31 and attack <= 40 then
        return "JAB"
    else
        return "NONE"
    end
end

-- Basic AI decision making (rule-based)
function makeDecision()
    local attack = detectOpponentAttack()
    
    -- Defensive strategy: dodge or block incoming attacks
    if attack == "LEFT_HOOK" then
        return "DODGE_RIGHT"
    elseif attack == "RIGHT_HOOK" then
        return "DODGE_LEFT"
    elseif attack == "UPPERCUT" then
        return "DUCK"
    elseif attack == "JAB" then
        return "BLOCK"
    elseif gameState.playerStamina > 50 and gameState.opponentHealth > 0 then
        -- Offensive: throw punches when safe
        if gameState.frameCounter % 30 < 15 then
            return "JAB_LEFT"
        else
            return "JAB_RIGHT"
        end
    else
        return "IDLE"
    end
end

-- Export game state (for external AI)
function exportGameState()
    return string.format(
        "%d,%d,%d,%d,%d,%d,%d,%d",
        gameState.playerHealth,
        gameState.playerStamina,
        gameState.playerStars,
        gameState.opponentHealth,
        gameState.opponentState,
        gameState.opponentAnim,
        gameState.opponentAttack,
        gameState.frameCounter
    )
end

-- Main loop
function mainLoop()
    updateGameState()
    
    -- Simple built-in AI
    local decision = makeDecision()
    executeMove(decision)
    
    -- Display debug info
    if gui then
        gui.text(10, 10, "Player HP: " .. gameState.playerHealth)
        gui.text(10, 25, "Opponent HP: " .. gameState.opponentHealth)
        gui.text(10, 40, "Decision: " .. decision)
        gui.text(10, 55, "State: " .. exportGameState())
    end
end

-- Register frame advance callback
if emu and emu.registerafter then
    emu.registerafter(mainLoop)
elseif emu and emu.registerbefore then
    emu.registerbefore(mainLoop)
else
    -- For BizHawk
    while true do
        mainLoop()
        emu.frameadvance()
    end
end

print("Punch-Out AI Agent loaded successfully!")
