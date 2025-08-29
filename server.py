import socket
import threading
import json

waiting_client = None
lock = threading.Lock()

def handle_client(conn, addr):
    global waiting_client
    print(f"[+] Client {addr} connected")

    try:
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break

            msg = json.loads(data)
            if msg["type"] == "play":
                choice = msg["choice"]

                with lock:
                    if waiting_client is None:
                        
                        waiting_client = (conn, choice)
                        conn.send(json.dumps({"type":"wait"}).encode())
                    else:
                        
                        other_conn, other_choice = waiting_client
                        winner_for_current = decide_winner(choice, other_choice)
                        winner_for_other = "draw" if winner_for_current=="draw" \
                                           else ("you" if winner_for_current=="opponent" else "opponent")

                        
                        conn.send(json.dumps({
                            "type":"result","you":choice,"opponent":other_choice,"winner":winner_for_current
                        }).encode())
                        other_conn.send(json.dumps({
                            "type":"result","you":other_choice,"opponent":choice,"winner":winner_for_other
                        }).encode())

                        waiting_client = None
    except Exception as e:
        print(f"[!] Error with {addr}: {e}")
    finally:
        conn.close()
        print(f"[-] Client {addr} disconnected")

def decide_winner(p1, p2):
    if p1 == p2:
        return "draw"
    if (p1=="Bua" and p2=="Keo") or \
       (p1=="Keo" and p2=="Bao") or \
       (p1=="Bao" and p2=="Bua"):
        return "you"
    return "opponent"

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 5000))   
    server.listen()
    print("[+] Server listening on 0.0.0.0:5000")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    start_server()