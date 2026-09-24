"""
LAB 3 CLIENT: Calls the remote procedures as if they were local functions.
Run server.py first, then run this.
"""

import xmlrpc.client

HOST = "127.0.0.1"
PORT = 65003

def main():
    # This "proxy" object IS the client stub -- every method call on it
    # gets marshaled and sent over the network automatically.
    proxy = xmlrpc.client.ServerProxy(f"http://{HOST}:{PORT}/")

    print("Calling remote add(4, 7)   ->", proxy.add(4, 7))
    print("Calling remote factorial(5)->", proxy.factorial(5))
    print("Calling remote reverse_string('distributed') ->",
          proxy.reverse_string("distributed"))

if __name__ == "__main__":
    main()
