# Authorized Local Port & Service Inspector

A defensive engineering tool built in Python for secure local asset validation, network baseline auditing, and testing environment inspection. **This repository contains code engineered exclusively for localhost self-inspections.**

## Purpose & Scope
This utility provides network administrators, engineers, and developers a lightweight mechanism to identify active listening services on their direct workstation or loopback addresses. It is designed to verify local configuration enforcement, ensure unnecessary development services are stopped, and audit open ports prior to system deployment.

## Ethical Boundaries & Guardrails
To prevent accidental misuse or unauthorized credentialing against remote networks, this toolkit includes an un-bypassable **Hardcoded Safety Guardrail**. 

* **Enforced Containment:** The execution context parses inputs against an exclusive loopback allowlist (`localhost`, `127.0.0.1`, `::1`). 
* **Scope Restriction:** Attempts to input external hostnames, public IP blocks, or adjacent network assets will cause immediate program termination.

```python
# Core Safety Guardrail in port_inspector.py
if target.lower() not in ALLOWED_TARGETS and resolved_ip not in ALLOWED_TARGETS:
    print("[-] SECURITY GUARDRAIL TRIGGERED: ... Scanning external networks is explicitly prohibited.")
    sys.exit(1)
```

## Quickstart Guide

### 1. Installation
Clone the repository and install the standard dependencies:
```bash
git clone https://github.com/<your-username>/local-port-inspector.git
cd local-port-inspector
pip install -r requirements.txt
```

### 2. Setting Up a Local Test Environment
To simulate an active local listening service, fire up the provided mock environment helper script in a separate terminal panel:
```bash
python mock_server.py
```

### 3. Executing the Inspector
Run the inspection tool against your loopback scope to parse active services:
```bash
python port_inspector.py --target 127.0.0.1 --ports 1-1000,8080
```

## Execution Examples

### Successful Local Diagnostic
```text
[*] Commencing defensive inspection on: 127.0.0.1 (127.0.0.1)
[*] Scanning 1001 ports using 100 threads...

[+] Scan Complete.

+--------+--------+-----------------+
|   Port | Status | Service         |
+========+========+=================+
|    135 | OPEN   | Unknown Service |
|    445 | OPEN   | SMB             |
|   8080 | OPEN   | HTTP-Alt        |
+--------+--------+-----------------+
```

### Guardrail Trigger Block
```text
$ python port_inspector.py --target example.com
[-] SECURITY GUARDRAIL TRIGGERED: This tool is strictly authorized
    for local self-inspection only (localhost / 127.0.0.1).
    Scanning external networks is explicitly prohibited.
```

## Screenshots
*(Place interactive output logs or command line terminal captures here during your deployment cycle)*

## License
Distributed under the MIT License. See `LICENSE` for more information.
