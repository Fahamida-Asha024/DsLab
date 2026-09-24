"""
Lab 2b: Limiting the Worker Pool
---------------------------------
This is the SOLUTION to the "bounded worker pool" exercise.

Builds on Lab 2's dispatcher/worker server. The dispatcher still accepts
every connection immediately, but now only MAX_WORKERS worker threads may
be doing their "work" (the 2-second simulated task) at the same time.
Extra clients are accepted right away but their worker threads block on
the semaphore until a slot frees up.
"""

import socket
import threading
import time

HOST = "127.0.0.1"
PORT = 65002
MAX_WORKERS = 2

# A Semaphore is like a Lock, but it hands out N permits instead of 1.
# Up to MAX_WORKERS threads can hold a permit at once; anyone else
# calling .acquire() (via the "with" statement) blocks until a permit
# is released.
worker_slots = threading.Semaphore(MAX_WORKERS)


def handle_client(conn, addr):
    """Runs inside its own thread -- one per client, same as Lab 2.
    The difference: before doing the slow work, it must first acquire
    a permit from worker_slots.
    """
    with conn:
        request = conn.recv(1024).decode()

        print(f"[WORKER-{threading.get_ident()}] Waiting for a free slot ({addr})")
        with worker_slots:  # blocks here if MAX_WORKERS threads are already inside
            print(f"[WORKER-{threading.get_ident()}] Got a slot, working on {addr}")
            time.sleep(2)  # simulate slow work (DB query, computation...)

            reply = f"Processed '{request}' by worker thread {threading.get_ident()}"
            conn.sendall(reply.encode())
            print(f"[WORKER-{threading.get_ident()}] Done with {addr}, releasing slot")


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((HOST, PORT))
        server_socket.listen(5)
        print(f"[DISPATCHER] Listening on {HOST}:{PORT} (max {MAX_WORKERS} concurrent workers)")

        while True:
            conn, addr = server_socket.accept()  # still accepts immediately, no change here
            print(f"[DISPATCHER] Accepted {addr}, spawning worker thread")
            worker = threading.Thread(target=handle_client, args=(conn, addr))
            worker.start()  # thread starts, but may block INSIDE on the semaphore


if __name__ == "__main__":
    main()
