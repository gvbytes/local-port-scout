# 🔍 Port Scanner (`port_scanner.py`)

## 💡 What is it?
This tool is a virtual port scanner. It connects to a target computer and checks which **ports** (virtual doorways) are open and waiting for connections.

---

## 🚪 The Analogy
Imagine you are walking around a large castle with 65,535 doors. Some doors are locked and sealed, some don't exist, and some are wide open with guards waiting inside to help visitors. A **Port Scanner** is like walking up to a list of doors and gently turning the handle to see if it turns (open) or if it is locked tight (closed).

---

## ⚙️ How it Works
1. **IP Address & Ports**: A computer has one IP address (like a street address) but thousands of ports (like apartment numbers). Websites listen on port 80/443, email on port 25, etc.
2. **The Handshake (TCP)**: The script uses Python's standard `socket` library to attempt a quick connection to a port. This is called a **TCP Three-Way Handshake**.
3. **The Result**: 
   * If the connection succeeds, the script prints that the port is **OPEN**.
   * If the connection times out or is refused, the port is **CLOSED**.
4. **Multithreading**: Instead of checking doors one by one (which takes a long time), the script spawns multiple "workers" (threads) to check many doors at the same time.

---

## 🛠️ Code Breakdown

* `socket.socket(socket.AF_INET, socket.SOCK_STREAM)`: Creates a new network socket using IPv4 and TCP.
* `s.connect_ex((host, port))`: Attempts to connect. Unlike `connect()`, which crashes the script if it fails, `connect_ex` returns a status number. A value of `0` means success (port is open).
* `threading.Thread(...)`: Runs the scanner logic concurrently, scanning hundreds of ports per second.

---

## 🚀 How to Run
Run the script and enter the host and port range you want to scan:
```bash
python port_scanner.py
```
*Note: For safety, this tool is restricted to scanning local hosts (like `localhost` or `127.0.0.1`) to prevent accidental scanning of remote systems.*
