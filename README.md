# Local Port Scout

## What it does
Local Port Scout checks a local or private host for open TCP ports. It is intentionally scoped for safe lab use and local network learning.

---

## How it works
1. **IP Address & Ports**: A computer has one IP address (like a street address) but thousands of ports (like apartment numbers). Websites listen on port 80/443, email on port 25, etc.
2. **The Handshake (TCP)**: The script uses Python's standard `socket` library to attempt a quick connection to a port. This is called a **TCP Three-Way Handshake**.
3. **The Result**: 
   * If the connection succeeds, the script prints that the port is **OPEN**.
   * If the connection times out or is refused, the port is **CLOSED**.
4. **Multithreading**: Instead of checking doors one by one (which takes a long time), the script spawns multiple "workers" (threads) to check many doors at the same time.

---

## Implementation notes

* `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`: Creates a new network socket using IPv4 and TCP.
* `s.connect_ex((host, port))`: Attempts to connect. Unlike `connect()`, which crashes the script if it fails, `connect_ex` returns a status number. A value of `0` means success (port is open).
* `threading.Thread(...)`: Runs the scanner logic concurrently, scanning hundreds of ports per second.

---

## Running it
Run the scanner against a local or private host:
```bash
python port_scanner.py
```
*Note: For safety, This script is restricted to scanning local hosts (like `localhost` or `127.0.0.1`) to prevent accidental scanning of remote systems.*


