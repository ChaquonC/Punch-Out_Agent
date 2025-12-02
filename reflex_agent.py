import socket

def run_server():
    sock = socket.socket()
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("127.0.0.1", 5001))
    sock.listen(1)

    print("Waiting for FCEUX...")
    conn, addr = sock.accept()
    print("Connected from", addr)

    mode = "WAITING"          # "WAITING", "DODGING", "ATTACKING"

    prev_health = None

    next_upper = "UPPER_LEFT"  # then UPPER_RIGHT, then back, etc.
    next_jab = "PUNCH_LEFT"

    while True:
        data = conn.recv(1024)
        if not data:
            break

        line = data.decode().strip()
        if not line:
            continue

        state_list = line.split(",")
        health         = int(state_list[0])
        opp_health     = int(state_list[1])
        opp_next_action = int(state_list[2])
        opp_action_timer = int(state_list[3])
        can_punch      = int(state_list[4])
        in_fight       = int(state_list[5])
        opp_knocked    = int(state_list[6])
        heart_lost         = int(state_list[7])

        took_damage = False
        if prev_health is not None and health < prev_health:
            took_damage = True

        # Default action
        action = "NONE"

        # If not actually fighting / opponent is down, do nothing
        if in_fight == 1 or opp_health <= 0 or opp_knocked == 1:
            mode = "WAITING"
            action = "NONE"

        elif health <= 0:
            action = next_jab
            next_upper = "PUNCH_RIGHT" if next_jab == "PUNCH_LEFT" else "PUNCH_LEFT"

        else:

            if mode == "WAITING":
                # sit still until enemy is about to swing
                if opp_action_timer < 10:
                    # Dodge first
                    mode = "DODGING"
                    action = "WAIT"
                else:
                    action = "NONE"

            elif mode == "DODGING":
                mode = "ATTACKING"
                action = "DODGE_LEFT"

            elif mode == "ATTACKING":
                # Stop attacking if hit or lose stamina
                if took_damage or heart_lost == 128:
                    mode = "WAITING"
                    action = "NONE"
                else:
                    if can_punch == 1:
                        action = next_upper
                        next_upper = "UPPER_RIGHT" if next_upper == "UPPER_LEFT" else "UPPER_LEFT"
                    else:
                        action = "NONE"

        # Send action to fceux
        conn.send((str(action) + "\n").encode())
        last_action = action

        prev_health = health

    conn.close()
    sock.close()

if __name__ == "__main__":
        run_server()
