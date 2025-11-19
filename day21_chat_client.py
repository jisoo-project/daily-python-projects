import socket
import threading
import sys


def receive(s):
    while True:
        try:
            data = s.recv(1024)
            if not data:
                print("[Client] Server closed connection.")
                return
            text = data.decode('utf-8', errors="replace").strip()
            print(f"\n{text}")
            print("You (Type '/quit' to exit): ", end="", flush=True)

        except socket.timeout:
            continue
        except OSError:
            return

def send(s, username):
    while True:
        try:
            message = input("You (Type '/quit' to exit): ").strip()
        except (EOFError, KeyboardInterrupt):
            message = "/quit"

        if message.lower() == "/quit":
            try:
                s.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            s.close()
            break

        full = f"<{username}> {message}"

        try:
            s.sendall(full.encode("utf-8"))
        except OSError:
            print("[Client] Connection lost.")
            return

def main():

    username = input("Enter your name: ").strip()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.7)
    try:
        s.connect(("127.0.0.1", 5555))
        print("Connected to chat server.")

        t_recv = threading.Thread(target=receive, args=(s,), daemon=True)
        t_send = threading.Thread(target=send, args=(s,username), daemon=True)
        t_recv.start()
        t_send.start()


        t_send.join()
    except ConnectionRefusedError:
        print("Connection failed (is the server running on 127.0.0.1:5555?).")
        sys.exit(1)
    finally:
        try:
            s.close()
        except OSError:
            pass

if __name__ == "__main__":
    main()