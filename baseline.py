logs = [
    "192.168.1.10 GET /index 200",
    "192.168.1.11 GET /login 200",
    "192.168.1.10 POST /login 401",
    "192.168.1.12 GET /index 200",
    "192.168.1.10 POST /login 200",
    "192.168.1.11 GET /admin 403",
    "192.168.1.12 GET /index 200",
]



def analyze_logs(logs: list[str]) -> dict:
    many = ["", 0]
    results = {
            "total_requests": 0,
            "error_count": 0,
            "requests_by_ip": {},
            "most_active_ip": None
    }

    for count, log in enumerate(logs, 1):
        ip = log.split()[0]
        error_code = int(log.split()[3])
        
        if ip not in results["requests_by_ip"]:
            results["requests_by_ip"][ip] = 1
        else:
            results["requests_by_ip"][ip] += 1

        if error_code >= 400:
            results["error_count"] += 1
        
        results["total_requests"] = count

    for k, v in results["requests_by_ip"].items():
        if v > many[1]:
            many[0] = k
            many[1] = v
    
    results["most_active_ip"] = many[0]

    return results


print(analyze_logs(logs))
