
import socket

def start_client():
    HOST = "127.0.0.1"
    PORT = 5000

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    print("[+] Connected to server")
    client.close()

if __name__ == "__main__":
    start_client()