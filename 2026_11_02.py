

tasks1 = ["deploy", "test", "build", "design"]

dependencies1 = [
    ("deploy", "test"),
    ("test", "build"),
    ("build", "design")
]

tasks2 = ["A", "B", "C", "D"]

dependencies2 = [
    ("D", "A"),
    ("D", "B"),
    ("C", "A")
]

tasks3 = ["A", "B", "C"]

dependencies3 = [
    ("A", "B"),
    ("B", "C"),
    ("C", "A")
]

tasks4 = ["A", "B"]

dependencies4 = [
    ("A", "C")
]


def resolve_tasks(
        tasks: list[str],
        dependencies: list[tuple[str, str]]
) -> list[str]:

    result = []
    explor = []
    is_recursion = False

    
    for depend in dependencies:
        child, parent = depend
        
        if parent not in tasks:
            return result
    
    for task in tasks:
        if task not in result:
            depend_judge(task, result, dependencies, explor, is_recursion)

    if is_recursion:
        result = []

    return result



def depend_judge(task, result, dependencies, explor, is_recursion):
    flag = False
    if is_recursion:
        return is_recursion

    if task in explor:
        return is_recursion

    explor.append(task)

    for depend in dependencies:
        child, parent = depend

        if task == child:
            flag = True
            depend_judge(parent, result, dependencies, explor, is_recursion)
            flag = False

    if flag == False:
        if task not in result:
            result.append(task)
            explor = []

    return result


def test_resolve_tasks():
    assert resolve_tasks(tasks1, dependencies1) == [
            "design", "build", "test", "deploy"
    ]

    assert resolve_tasks(tasks2, dependencies2) == [
            "A", "B", "C", "D"
    ]

    assert resolve_tasks(tasks3, dependencies3) == []

    assert resolve_tasks(tasks4, dependencies4) == []

print(resolve_tasks(tasks1, dependencies1))
