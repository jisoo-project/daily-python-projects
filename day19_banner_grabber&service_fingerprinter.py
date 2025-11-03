import socket
import sys
import time

host = input("Host: ").strip()
ports_str = input("Ports (comma-separated): ").strip()

tokens = [t.strip() for t in ports_str.split(",") if t.strip()]
ports_list = []

for t in tokens:
    if not t.isdigit():
        print(f"Invalid port token: {t}")
        sys.exit(1)
    p = int(t)
    if not (1 <= p <= 65535):
        print(f"Port out of range (1-65535): {p}")
        sys.exit(1)
    ports_list.append(p)

ports_list = sorted(set(ports_list))
if not ports_list:
    print("No valid ports provided.")
    sys.exit(1)

try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Invalid host.")
    sys.exit(1)

print(f"[+] Scanning {host} ({ip}) ports: {', '.join(map(str, ports_list))}")

open_ports = {}
HTTP_PORTS = (80, 81, 8000, 8008, 8080, 8088, 8888)
probe_enabled = True
start = time.time()
for port in ports_list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.7)
    try:
        code = s.connect_ex((ip, port))
        if code != 0:
            continue
        try:
            data = s.recv(1024)
        except socket.timeout:
            data = b""
        if (not data) and probe_enabled and (port in HTTP_PORTS):
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\nHost: example\r\n\r\n")
                data = s.recv(1024)
            except socket.timeout:
                data = b""

        if data:
            banner = data.decode("utf-8", errors="replace").strip()
            banner = banner.replace("\r\n", "\n").replace("\r", "\n")
            banner = banner[:200]

        else:
            banner = "no banner"

        open_ports[port] = banner

    finally:
        s.close()


elapsed = time.time() - start

if not open_ports:
    print("No open ports found.")
    print(f"Scan completed in {elapsed:.2f} seconds")
    sys.exit(0)


print(f"Results ({len(open_ports)} open): ")
for p in sorted(open_ports):
    print(f"- {p}: {open_ports[p]}")
print(f"Scan completed in {elapsed:.2f} seconds")
