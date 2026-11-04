logs = [
    ("alice", 100),
    ("bob", 200),
    ("alice", 110),
    ("alice", 160),
    ("bob", 220),
    ("alice", 120),
    ("bob", 300),
    ("alice", 170)
]

timeout = 30

logs2 = [
    ("A", 0),
    ("A", 25),
    ("A", 50),
    ("A", 75)
]

timeout2 = 30

logs3 = [
    ("A", 100),
    ("A", 100),
    ("A", 130),
    ("A", 161)
]

timeout3 = 30

logs4 = []
timeout4 = 30

logs5 = [
    ("A", 100)
]
timeout5 = 30


def analyze_sessions(
        logs: list[tuple[str, int]],
        timeout: int
) -> dict[str, list[tuple[int, int, int]]]:
    
    person = {}
    results = {}

    # 同一ユーザーのアクセス履歴をまとめる    
    for log in logs:
        name, access_time = log

        if name not in person:
            person[name] = []

        person[name].append(access_time)

    for name, person_log in person.items():
        person_log.sort()
        session = []
        count = 0
        index = 0

        while count < len(person_log):
            access_num = 0
            session.append([person_log[count]])
            count, access_num = session_judge(person_log, timeout, count, access_num)
            session[index].extend([person_log[count], access_num]) # 末尾の操作は[-1]を使うこともできる
            session[index] = tuple(session[index])
            index += 1
            count += 1
 
        results[name] = session     

    return results

def session_judge(person_log, timeout, count, access_num):
    access_num += 1

    if count >= len(person_log) - 1:
        return count, access_num
    if person_log[count + 1] - person_log[count] > timeout:
        return count, access_num
    else:
        count += 1
        return session_judge(person_log, timeout, count, access_num)



def test_analyze_sessions():
    assert analyze_sessions(logs, timeout) == {
            "alice": [
                (100, 120, 3),
                (160, 170, 2)
            ],
            "bob": [
                (200, 220, 2),
                (300, 300, 1)
            ]
    }

    assert analyze_sessions(logs2, timeout2) == {"A": [(0, 75, 4)]}
    
    assert analyze_sessions(logs3, timeout3) == {
            "A": [
                (100, 130, 3),
                (161, 161, 1)
            ]
    }

    assert analyze_sessions(logs4, timeout4) == {}

    assert analyze_sessions(logs5, timeout5) == {"A": [(100, 100, 1)]}


