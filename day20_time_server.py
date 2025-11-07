import socket
import sys
import datetime
import signal
from typing import Optional
from types import FrameType

def parse_port():
    if len(sys.argv) >= 2:
        try:
            p = int(sys.argv[1])
            if 1 <= p <= 65535:
                return p
        except ValueError:
            pass
        print("Usage: python time_server.py [port]")
        sys.exit(1)
    return 2323

def make_time_banner():
    now = datetime.datetime.now(datetime.UTC).replace(microsecond=0).isoformat()
    return f"TIME {now}\n".encode("utf-8")

def make_error():
    return b"ERROR unsupported\n"

def handle_sigint(sig: int, frame: Optional[FrameType]) -> None:
    raise KeyboardInterrupt


def main():
    port = parse_port()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind(("0.0.0.0", port))
    server.listen(5)
    print(f"[time_server] Listening on 0.0.0.0:{port} (Ctrl+C to stop)")

    signal.signal(signal.SIGINT, handle_sigint)

    try:
        while True:
            conn, addr = server.accept()
            try:
                conn.settimeout(0.5)
                try:
                    data = conn.recv(1024)
                except socket.timeout:
                    data = b""
                if not data:
                    conn.sendall(make_time_banner())
                    continue
                text = data.decode("utf-8", errors="replace").strip()
                if text.lower() == "time":
                    conn.sendall(make_time_banner())
                else:
                    conn.sendall(make_error())
            finally:
                conn.close()
    except KeyboardInterrupt:
        print("\n[time_server] Shutting down.")
    finally:
        server.close()

if __name__ == "__main__":
    main()