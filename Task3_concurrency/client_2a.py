"""
Lab 2b: Limiting the Worker Pool -- Client
--------------------------------------------
Unchanged from Lab 2's client. Fires N near-simultaneous requests at the
server so you can observe how the bounded worker pool changes the total
completion time.

With MAX_WORKERS = 2 on the server and N = 5 clients here, each taking
2 seconds of simulated work, expect roughly:
    Clients 1 & 2 -> finish around 2s
    Clients 3 & 4 -> finish around 4s
    Client 5      -> finishes around 6s
So total time should land around ~6 seconds.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65002
N = 100  # number of "simultaneous" clients


def worker(i):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(f"request-{i}".encode())
        reply = s.recv(1024).decode()
        print(f"[CLIENT {i}] {reply}")


def main():
    start = time.time()
    threads = [threading.Thread(target=worker, args=(i,)) for i in range(N)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    elapsed = time.time() - start
    print(f"\nAll {N} requests completed in {elapsed:.2f} seconds")
    print("(With MAX_WORKERS = 2 on the server, expect roughly 6s, not ~2s or ~10s)")


if __name__ == "__main__":
    main()
