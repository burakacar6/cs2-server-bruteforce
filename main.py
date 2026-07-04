import a2s
import ipaddress
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed

TARGET_SERVER_NAMES = ['CS2']  
TIMEOUT = 1 
MAX_WORKERS = 2000  

def get_server_info(ip, port):
    try:
        server_info = a2s.info((ip, port), timeout=TIMEOUT)
        return {
            "name": getattr(server_info, "server_name", None),
            "ip": ip,
            "port": port
        }
    except Exception:
        return None

def brute_force_servers(ip_range, ports, max_workers=MAX_WORKERS):
    """Brute force scan IP range and ports for target server"""
    found_servers = []
    
    try:
        network = ipaddress.ip_network(ip_range, strict=False)
    except ValueError:
        print(f"Invalid IP range: {ip_range}")
        return found_servers
    
    ips = list(network.hosts()) if network.num_addresses > 2 else [network.network_address, network.broadcast_address]
    
    total_targets = len(ips) * len(ports)
    scanned = 0
    
    print(f"[*] Starting brute force scan on {ip_range}")
    print(f"[*] Target IPs: {len(ips)}, Ports: {len(ports)}, Total combinations: {total_targets}")
    print(f"[*] Looking for: {', '.join(TARGET_SERVER_NAMES)}\n")
    
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = {}
        for ip in ips:
            for port in ports:
                future = executor.submit(get_server_info, str(ip), port)
                futures[future] = (str(ip), port)
        
        for future in as_completed(futures):
            scanned += 1
            ip, port = futures[future]
            result = future.result()
            
            if result and result.get("name"):
                server_name = result.get("name").lower()
                for target in TARGET_SERVER_NAMES:
                    if target.lower() in server_name:
                        print(f"[+] FOUND: {ip}:{port} | {result['name']}")
                        found_servers.append((ip, port))
                        break
            
            if scanned % 100 == 0:
                print(f"[*] Scanned {scanned}/{total_targets}...")
    
    print(f"\n[*] Scan complete! Found {len(found_servers)} server(s)")
    return found_servers

if __name__ == "__main__":
    ip_range = "x.x.x.x/xx" # subnet 
    ports = [27015, 27016, 27017, 27018, 27019, 27020, 27030, 27031, 27032, 27033]
    
    print("=== Game Server Brute Force Scanner ===\n")
    
    servers = brute_force_servers(ip_range, ports)
    
    if servers:
        print("\n[=] Summary of found servers:")
        for ip, port in servers:
            print(f"  - {ip}:{port}")