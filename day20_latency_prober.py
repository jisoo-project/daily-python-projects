import socket
import sys
import time

host = input("Host: ").strip()
ports = input("Ports (comma-separated): ").strip()

tokens = [t.strip() for t in ports.split(",") if t.strip()]
ports_list = []
for t in tokens:
    if not t.isdigit():
        print("Invalid port.")
        sys.exit(1)
    p = int(t)
    if not 1 <= p <= 65535:
        print("Port out of range (1-65535).")
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

print(f"[+] Probing {host} ({ip}): {', '.join(map(str, ports_list))}")

ports_status = []
HTTP_PORTS = (80, 81, 8000, 8008, 8080, 8088, 8888)

t0 = time.time()
for port in ports_list:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.7)
    try:
        t1 = time.time()
        code = s.connect_ex((ip, port))
        if code != 0:
            latency = time.time() - t1
            ports_status.append((port, "CLOSED", latency, "-"))
            continue
        try:
            data = s.recv(1024)
        except socket.timeout:
            data = b""
        if not data and port in HTTP_PORTS:
            try:
                s.sendall(b"HEAD / HTTP/1.0\r\nHost: example\r\n\r\n")
                data = s.recv(1024)
            except socket.timeout:
                data = b""
        if not data:
            try:
                s.sendall(b"TIME\n")
                data = s.recv(1024)
            except socket.timeout:
                data = b""
        if data:
            banner = data.decode("utf-8", errors='replace')
            banner = banner.replace("\r\n", "\n").replace("\r", "\n")
            banner = banner[:200].strip()
        else:
            banner = "no banner"

        latency = time.time() - t1
        ports_status.append((port, "OPEN", latency, banner))

    finally:
        s.close()

elapsed = time.time() - t0

for port, status, latency, banner in ports_status:
    if isinstance(latency, (int, float)):
        latency_display = f"{latency*1000:.1f} ms"
    else:
        latency_display = str(latency)
    print(f"port {port:<5} | {status:<6} | {latency_display:<10} | {banner}")

print(f"Scan completed in {elapsed:.2f} s")

