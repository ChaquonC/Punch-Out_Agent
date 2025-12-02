local ENV = dofile("env.lua")
-- package path
package.path = ENV.PATH
-- package core
package.cpath = ENV.COREPATH

local socket = require("socket")
local client = socket.tcp()
client:connect("127.0.0.1", 5001)
client:settimeout(nil)

local hp_addr = 0x0392

function button_press(joypad_config)
    joypad.set(1, joypad_config)
    emu.frameadvance()
    joypad.set(1, joypad_config)
    emu.frameadvance()
    joypad.set(1, joypad_config)
    emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
     emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
    joypad.set(1, {})
    emu.frameadvance()
end

function wait(n)
    print("waiting")
    for i = 1, n do
        emu.frameadvance()
    end
end

PUNCH_OUT_ACTIONS = {
    NONE              = {},
    PUNCH_RIGHT       = {A=true},
    PUNCH_LEFT        = {B=true},
    UPPER_RIGHT       = {up=true, A=true},
    UPPER_LEFT        = {up=true, B=true},
    BLOCK             = {down=true},
    DODGE_LEFT        = {left=true},
    DODGE_RIGHT       = {right=true},
    START             = {start=true},
}

STATE = {
    health = 0,
    opponent_health = 0,
    opponent_next_action = 0,
    opponent_next_action_timer = 100,
    can_punch = 0,
    in_fight = 0,
    opp_knocked_down = 0,
    heart_lost = 0
}

function read_state()
    STATE.health = memory.readbyte(0x0397)
    STATE.opponent_health = memory.readbyte(0x0399)
    STATE.opponent_next_action = memory.readbyte(0x003A)
    STATE.opponent_next_action_timer = memory.readbyte(0x0039)
    STATE.can_punch = memory.readbyte(0x00BC)
    STATE.in_fight = memory.readbyte(0x0004)
    STATE.opp_knocked_down = memory.readbyte(0x0005)
    STATE.heart_lost = memory.readbyte(0x0393)
end

function state_to_csv()
    return table.concat({
        STATE.health,
        STATE.opponent_health,
        STATE.opponent_next_action,
        STATE.opponent_next_action_timer,
        STATE.can_punch,
        STATE.in_fight,
        STATE.opp_knocked_down,
        STATE.heart_lost
    }, ",")
end


while true do
    read_state()
    local csv = state_to_csv()
    client:send(csv .. "\n")

    local line = client:receive("*l")
    print(string.format("action: %s", line))
    local action = PUNCH_OUT_ACTIONS[line] or PUNCH_OUT_ACTIONS.NONE

    button_press(action)

    if action ~= PUNCH_OUT_ACTIONS.NONE then
        button_press(action)
    elseif line == "WAIT" then
        -- local time = client:receive("*l")
        wait(45)
    else
        joypad.set(1, {})
        emu.frameadvance()
    end
end
