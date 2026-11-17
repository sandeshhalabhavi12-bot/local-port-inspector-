import socket
import sys
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from tabulate import tabulate

# Strict Local Safety Guardrail
ALLOWED_TARGETS = {"localhost", "127.0.0.1", "::1"}

COMMON_PORTS = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
    80: "HTTP", 110: "POP3", 143: "IMAP", 443: "HTTPS", 445: "SMB",
    1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 5432: "PostgreSQL",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt"
}

def verify_target(target):
    """Enforces the defensive scope by blocking non-loopback scanning."""
    try:
        resolved_ip = socket.gethostbyname(target)
    except socket.gaierror:
        print(f"[-] Error: Unable to resolve target '{target}'")
        sys.exit(1)
        
    if target.lower() not in ALLOWED_TARGETS and resolved_ip not in ALLOWED_TARGETS:
        print("[-] SECURITY GUARDRAIL TRIGGERED: This tool is strictly authorized")
        print("    for local self-inspection only (localhost / 127.0.0.1).")
        print("    Scanning external networks is explicitly prohibited.")
        sys.exit(1)
    return resolved_ip

def scan_port(target, port, timeout):
    """Attempts to connect to a specific port to determine its state."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(timeout)
            result = s.connect_ex((target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown Service")
                return {"Port": port, "Status": "OPEN", "Service": service}
    except Exception:
        pass
    return None

def main():
    parser = argparse.ArgumentParser(
        description="Authorized Local Port & Service Inspector (Defensive Audit Tool)"
    )
    parser.add_argument("-t", "--target", default="127.0.0.1", help="Target host (Strictly limited to localhost)")
    parser.add_argument("-p", "--ports", default="1-1024", help="Port range to scan (e.g., 80,443 or 1-1024)")
    parser.add_argument("--timeout", type=float, default=1.0, help="Connection timeout in seconds")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads")
    args = parser.parse_args()

    target_ip = verify_target(args.target)
    
    # Parse port range or list
    ports_to_scan = []
    try:
        if "-" in args.ports:
            start, end = map(int, args.ports.split("-"))
            ports_to_scan = list(range(start, end + 1))
        else:
            ports_to_scan = [int(p.strip()) for p in args.ports.split(",")]
    except ValueError:
        print("[-] Error: Invalid port format. Use notation like '80,443' or '1-1024'.")
        sys.exit(1)

    print(f"[*] Commencing defensive inspection on: {args.target} ({target_ip})")
    print(f"[*] Scanning {len(ports_to_scan)} ports using {args.threads} threads...")

    open_ports = []
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = {executor.submit(scan_port, target_ip, port, args.timeout): port for port in ports_to_scan}
        for future in as_completed(futures):
            res = future.result()
            if res:
                open_ports.append(res)

    print("\n[+] Scan Complete.\n")
    if open_ports:
        open_ports.sort(key=lambda x: x["Port"])
        print(tabulate(open_ports, headers="keys", tablefmt="grid"))
    else:
        print("[*] No open ports identified within the designated scope.")

if __name__ == "__main__":
    main()
