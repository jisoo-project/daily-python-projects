import requests
import datetime

urls_file = "urls.txt"
results_file = "results.txt"
today_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

try:
    with open(urls_file, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip()]
except FileNotFoundError:
    lines = []

print("=== URL Status Checker ===")

if not lines:
    print("No urls yet.")
else:
    print(f"Loaded {len(lines)} URLs to check.")
    for line in lines:
        url = line

        try:
            response = requests.get(url, timeout=5)
            ms = response.elapsed.total_seconds() * 1000
            status_code = response.status_code
            print(f"[OK] {status_code} {ms:.0f}ms {url}")
            with open(results_file, "a") as f:
                f.write(f"{today_time} | {status_code} | {ms:.0f} | {url}\n")
        except requests.RequestException:
            print(f"[FAIL] ERROR - {url}")
            with open(results_file, "a") as f:
                f.write(f"{today_time} | ERROR | - | {url}\n")

    print("=== Summary ===")

    with open(results_file, "r") as f:
        lines = [ln.strip() for ln in f if ln.strip()]

    total = len(lines)

    time_list = []
    status_dict = {"OK":0, "FAIL":0}

    for line in lines:
        parts = [p.strip() for p in line.split("|")]
        if len(parts) < 3:
            continue
        today, status, time = parts[:3]
        if time != "-":
            time_list.append(int(time))
        if status == "ERROR":
            status_dict["FAIL"] += 1
        else:
            status_dict["OK"] += 1

    avg_time = (sum(time_list) / len(time_list)) if time_list else 0.0

    print(f" Total: {total} | OK: {status_dict['OK']} | FAIL: {status_dict['FAIL']} | Avg time: {avg_time:.2f} ms")
    print(f"(Appended {total} lines to results.txt)")











