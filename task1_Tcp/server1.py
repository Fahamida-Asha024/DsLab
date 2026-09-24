"""
LAB 1: The Client-Server Model (maps to Lecture 1)
----------------------------------------------------
Goal: Demonstrate the basic request-reply interaction between an
independent client process and a server process, over TCP sockets.

Concepts you should observe / write about in your report:
- Server WAITS passively for requests (concept from Lec 1, slide 11)
- Client actively SENDS a request and blocks until a reply arrives
- The two processes are independent programs, possibly on different
  machines, that only interact via messages (no shared memory)
- This is a SEQUENTIAL server: it handles one client fully before
  accepting the next. Keep this in mind -- Lab 2 fixes this limitation.
"""

import socket

HOST = "127.0.0.1"   # localhost -- change to your machine's IP to test
PORT = 65001          # across two real machines on the same network

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Allow quick restarts without "Address already in use" errors
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[SERVER] Listening on {HOST}:{PORT} ... waiting for requests")

        while True:
            conn, addr = server_socket.accept()   # BLOCKS here (passive wait)
            with conn:
                print(f"[SERVER] Connection from {addr}")
                request = conn.recv(1024).decode()
                print(f"[SERVER] Received request: {request!r}")

                # "Processing" the request -- here we just uppercase it,
                # but imagine this being a database lookup, a file read, etc.
                reply = f"ECHO: {request.upper()}"

                conn.sendall(reply.encode())
                print(f"[SERVER] Sent reply: {reply!r}\n")

if __name__ == "__main__":
    main()
