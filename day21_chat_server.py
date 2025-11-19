import socket
import threading
import signal
from typing import Optional
from types import FrameType

clients = []

def handle_client(con, addr):
    print(f"[Server] New connection from {addr[0]}:{addr[1]}")
    con.settimeout(1.0)
    try:
        while True:
            try:
                data = con.recv(1024)
                if not data:
                    print(f"[Server] {addr[0]}:{addr[1]} disconnected")
                    clients.remove(con)
                    break
                for c in clients:
                    if c is not con:
                        c.sendall(data + b"\n")
                text = data.decode("utf-8", errors="replace").strip()
                if text:
                    print(f"[Server] Broadcasting message: {text}")
            except socket.timeout:
                continue
    except Exception as e:
        print(f"[Server] Error with: {addr}: {e}")
    finally:
        con.close()

def handle_interrupt(sig: int, frame: Optional[FrameType]) -> None:
    raise KeyboardInterrupt

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("127.0.0.1", 5555))
    server.listen(5)
    print("[Server] Listening on port 5555 (Ctrl+C to stop)")
    signal.signal(signal.SIGINT, handle_interrupt)
    try:
        while True:
            con, addr = server.accept()
            clients.append(con)

            threading.Thread(target=handle_client, args=(con, addr), daemon=True).start()

    except KeyboardInterrupt:
        print("\n[Server] Shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    main()