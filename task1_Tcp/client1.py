"""
LAB 1: The Client-Server Model -- CLIENT SIDE
Run server.py first, then run this in a second terminal.
You can run this client multiple times, or from a different machine
pointed at the server's real IP address, to see the request-reply
pattern repeat.
"""

import socket

HOST = "127.0.0.1"
PORT = 65001

def send_request(message: str):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((HOST, PORT))
        print(f"[CLIENT] Sending: {message!r}")
        client_socket.sendall(message.encode())

        reply = client_socket.recv(1024).decode()
        print(f"[CLIENT] Received: {reply!r}")

if __name__ == "__main__":
    send_request("hello distributed systems")
