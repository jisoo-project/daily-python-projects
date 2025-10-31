import socket
import sys
import time

host = input("Enter target host: ")
start_port = input("Enter start port: ")
end_port = input("Enter end port: ")

try:
    start = int(start_port); end = int(end_port)
except ValueError:
    print("Please enter a number.")
    sys.exit(1)

if not 1<= start <= end <= 65535:
    print("Invalid port.")
    sys.exit(1)

try:
    ip = socket.gethostbyname(host)
except socket.gaierror:
    print("Invalid host.")
    sys.exit(1)

print(f"[+] Scanning {start_port}-{end_port} on {host}. . .")

open_ports = []
start_time = time.time()
for port in range(start, end+1):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.7)
    code = s.connect_ex((ip, port))
    s.close()
    if code == 0:
        open_ports.append(port)

elapsed = time.time() - start_time

services = {
  21:"FTP", 22:"SSH", 23:"Telnet", 25:"SMTP", 53:"DNS",
  80:"HTTP", 110:"POP3", 143:"IMAP", 443:"HTTPS", 3389:"RDP"
}

if not open_ports:
    print("No open ports found.")
    sys.exit(0)

print(f"Open ports ({len(open_ports)}):")
for p in open_ports:
    print(f"- {p}: {services.get(p,'unknown')}")
print(f"Scan completed in {elapsed:.2f} seconds")













