import argparse
import ipaddress
import queue
import socket
import sys
import threading
import time

# Thread-safe print lock to prevent overlapping output
print_lock = threading.Lock()

def is_local_or_loopback(host):
    """
    Resolves the host and verifies if it is a loopback or private/local IP address.
    This restricts the script to safe testing environments.
    """
    try:
        ip_str = socket.gethostbyname(host)
        ip = ipaddress.ip_address(ip_str)
        return ip.is_loopback or ip.is_private
    except Exception:
        return False

def scan_port(host, port, timeout):
    """
    Attempts to establish a TCP connection to the specified port.
    Uses socket.connect_ex which returns 0 on success (connection established)
    instead of raising an exception, making it faster and cleaner for scanning.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    # connect_ex performs the standard TCP three-way handshake (SYN, SYN-ACK, ACK).
    # If the handshake completes, it returns 0 (port open).
    # If it is blocked or closed, it returns an error code (e.g., connection timed out or refused).
    result = s.connect_ex((host, port))
    s.close()
    return result == 0

def worker(host, port_queue, timeout, open_ports):
    while True:
        try:
            port = port_queue.get_nowait()
        except queue.Empty:
            break
        
        if scan_port(host, port, timeout):
            with print_lock:
                print(f"[+] Port {port:<5} is OPEN")
                sys.stdout.flush()
            open_ports.append(port)
        port_queue.task_done()

def main():
    parser = argparse.ArgumentParser(description="Multithreaded TCP Port Scanner (Local/Loopback Only)")
    parser.add_argument("host", nargs="?", help="Target host (IP or domain)")
    parser.add_argument("--start", type=int, default=1, help="Start port")
    parser.add_argument("--end", type=int, default=1024, help="End port")
    parser.add_argument("--threads", type=int, default=100, help="Number of concurrent threads")
    parser.add_argument("--timeout", type=float, default=1.0, help="Socket timeout in seconds")
    
    args = parser.parse_args()
    
    host = args.host
    if not host:
        host = input("Enter target host: ").strip()
    
    if not host:
        print("[-] Error: Host is required.")
        sys.exit(1)
        
    if not is_local_or_loopback(host):
        print("[-] Error: Target must resolve to a local or loopback address (e.g., localhost, 127.0.0.1, 192.168.x.x).")
        sys.exit(1)

    start_port = args.start
    end_port = args.end
    
    if not args.host:
        try:
            start_port = int(input(f"Enter start port (default {start_port}): ") or start_port)
            end_port = int(input(f"Enter end port (default {end_port}): ") or end_port)
        except ValueError:
            print("[-] Error: Ports must be integers.")
            sys.exit(1)

    if start_port < 1 or end_port > 65535 or start_port > end_port:
        print("[-] Error: Invalid port range.")
        sys.exit(1)

    print(f"\n[*] Scanning target: {host} (IP: {socket.gethostbyname(host)})")
    print(f"[*] Port range: {start_port} - {end_port}")
    print(f"[*] Threads: {args.threads} | Timeout: {args.timeout}s\n")
    
    port_queue = queue.Queue()
    for port in range(start_port, end_port + 1):
        port_queue.put(port)
        
    open_ports = []
    threads = []
    
    start_time = time.time()
    
    # Spawn worker threads
    num_threads = min(args.threads, port_queue.qsize())
    for _ in range(num_threads):
        t = threading.Thread(target=worker, args=(host, port_queue, args.timeout, open_ports))
        t.daemon = True
        t.start()
        threads.append(t)
        
    # Wait for queue to be empty
    port_queue.join()
    
    # Wait for all threads to finish
    for t in threads:
        t.join()
        
    duration = time.time() - start_time
    print(f"\n[*] Scan completed in {duration:.2f} seconds.")
    print(f"[*] Open ports found: {sorted(open_ports)}")

if __name__ == "__main__":
    main()
