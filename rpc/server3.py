"""
LAB 3: Remote Procedure Call (maps to Lecture 4)
---------------------------------------------------
Goal: Show RPC transparency -- the client calls a function that LOOKS
local, but actually runs on this remote server process.

Python's xmlrpc module gives you both halves of the stub pair for free:
  - The library auto-generates the SERVER STUB that receives the marshaled
    call, unpacks (unmarshals) the parameters, and invokes the real function.
  - The library auto-generates the CLIENT STUB (a "proxy" object) that
    marshals your arguments into XML and sends them over HTTP.
This is exactly the client-stub/server-stub picture from Lec 4, slide 4 --
you just don't have to hand-write the stubs yourself.
"""

from xmlrpc.server import SimpleXMLRPCServer

HOST = "127.0.0.1"
PORT = 65003

# ---- These are the "remote procedures" the client will call ----

def add(a, b):
    print(f"[SERVER] add({a}, {b}) called remotely")
    return a + b

def factorial(n):
    print(f"[SERVER] factorial({n}) called remotely")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

def reverse_string(s):
    print(f"[SERVER] reverse_string({s!r}) called remotely")
    return s[::-1]

def main():
    server = SimpleXMLRPCServer((HOST, PORT), allow_none=True)
    server.register_function(add, "add")
    server.register_function(factorial, "factorial")
    server.register_function(reverse_string, "reverse_string")
    print(f"[SERVER] RPC server listening on {HOST}:{PORT}")
    print("[SERVER] Exposed procedures: add, factorial, reverse_string")
    server.serve_forever()

if __name__ == "__main__":
    main()
