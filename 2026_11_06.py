def search_tasks(
        tasks: list[dict],
        statuses: set[str],
        min_priority: int,
        keyword: str,
        limit: int
        ) -> list[dict]:

    searched = {}
    source_tasks = {}
    result = []

    for task in tasks:
        source_tasks[task["id"]] = task.copy()

    for task in tasks:
        id, priority = condition_search(task, statuses, keyword, min_priority)
        if id != 0:
            searched[id] = priority

    sorted_tasks = sort_searched_tasks(searched, min_priority)

    if not sorted_tasks:
        return []

    else:
        for i in sorted_tasks:
            result.append(source_tasks[i])

        return result[:limit]

def condition_search(
        task: dict,
        statuses: set[str],
        keyword: str,
        min_priority
        ):
    
    status = task["status"]
    priority = task["priority"]
    title = task["title"]

    if len(statuses) != 0:
        if status not in statuses:
            return 0, 0

    if priority < min_priority:
        return 0, 0
    
    if len(keyword) != 0:
        if keyword.lower() not in title.lower():
            return 0, 0

    return task["id"], task["priority"]

def sort_searched_tasks(searched, min_priority):
    sorted = []
    now_priority = 5   

    while now_priority >= min_priority:
        now = []
        for id, priority in searched.items():
            if priority == now_priority:
                now.append(id)

        now.sort()
        sorted.extend(now)

        now_priority -= 1

    return sorted
        
# --- test ---

tasks = [
    {"id": 3, "title": "Write tests", "status": "todo", "priority": 2},
    {"id": 1, "title": "Fix login", "status": "doing", "priority": 3},
    {"id": 4, "title": "Write docs", "status": "done", "priority": 3},
    {"id": 2, "title": "Fix API", "status": "todo", "priority": 3},
    {"id": 5, "title": "Review code", "status": "todo", "priority": 1}
]

statuses = {"todo", "doing"}
min_priority = 2
keyword = "fix"
limit = 5

tasks2 = [
    {"id": 5, "title": "Task A", "status": "done", "priority": 1},
    {"id": 2, "title": "Task B", "status": "todo", "priority": 3},
    {"id": 3, "title": "Task C", "status": "doing", "priority": 3}
]

statuses2 = set()
min_priority2 = 1
keyword2 = ""
limit2 = 10

tasks3 = [
    {"id": 1, "title": "Write tests", "status": "todo", "priority": 2}
]

statuses3 = {"done"}
min_priority3 = 3
keyword3 = "fix"
limit3 = 5

tasks4 = []


def test_search_tasks():
    assert search_tasks(tasks, statuses, min_priority, keyword, limit) == [
        {"id": 1, "title": "Fix login", "status": "doing", "priority": 3},
        {"id": 2, "title": "Fix API", "status": "todo", "priority": 3}
    ]

    assert search_tasks(tasks2, statuses2, min_priority2, keyword2, limit2) == [
        {"id": 2, "title": "Task B", "status": "todo", "priority": 3},
        {"id": 3, "title": "Task C", "status": "doing", "priority": 3},
        {"id": 5, "title": "Task A", "status": "done", "priority": 1}
    ]

    assert search_tasks(tasks3, statuses3, min_priority3, keyword3, limit3) == []

    assert search_tasks(tasks4, statuses, min_priority, keyword, limit) == []
