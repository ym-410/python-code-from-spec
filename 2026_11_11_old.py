import copy


def detect_incidents(
        logs: list[tuple[int, str, int]],
        window: int,
        threshold: int
): # -> list[tuple[str, int, int ,int]]:
    
    tmp_logs = logs.copy()
    sorted_logs = sorted(tmp_logs)
    incident = {}
    result_incident = []
    is_incident = {}
    default_target_logs = {}
    
    for log in sorted_logs:
        if log[1] not in is_incident:
            is_incident[log[1]] = False
        
        if log[1] not in default_target_logs:
            default_target_logs[log[1]] = []
    
    
    for log in sorted_logs:
        target_logs = copy.deepcopy(default_target_logs)
        time, service, status_code = log

        target_time_start = time - window
        target_time_end = time

        for check_log in sorted_logs:
            if target_time_start < check_log[0] <= target_time_end:
                if check_log[2] >= 500:
                    if check_log[1] not in target_logs:
                        target_logs[check_log[1]] = []
                    target_logs[check_log[1]].append(check_log)

        # 障害判定
        if is_incident[service] == False:

            if len(target_logs[service]) >= threshold:
                peak_errors = len(target_logs[service])
                incident_start = target_logs[service][-1][0]
                incident[service] = [service, incident_start, incident_start, peak_errors]
                is_incident[service] = True

        else:

            if len(target_logs[service]) < threshold:
                result_incident.append(incident[service])
                del incident[service]
                is_incident[service] = False
                peak_errors = 0

            else:
                if len(target_logs[service]) > incident[service][3]:
                    peak_errors = len(target_logs[service])
                    incident[service][3] = peak_errors
                incident_end = time
                incident[service][2] = incident_end

    for service in is_incident:
        if is_incident[service]:
            result_incident.append(incident[service])
            del incident[service]
            is_incident[service] = False

    sorted_result_incident = sorted(result_incident, key=lambda x: x[1])

    return sorted_result_incident
                    


# -- test --
logs = [
    (10, "api", 500),
    (12, "api", 502),
    (15, "api", 503),
    (18, "api", 200),
    (25, "api", 200),
    (30, "api", 500),
]

window = 10
threshold = 3

print(detect_incidents(logs, window, threshold))
