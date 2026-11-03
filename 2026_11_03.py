records = [
    ("Alice", "Math", 90),
    ("Bob", "Math", 70),
    ("Alice", "English", 80),
    ("Bob", "English", 55),
    ("Charlie", "Math", 95),
    ("Alice", "History", 100),
    ("Charlie", "English", 85)
]

required_subjects = {"Math", "English"}
threshold = 80.0

records2 = [
    ("A", "Math", 100),
    ("B", "Math", 90),
    ("B", "English", 80)
]

required_subjects2 = {"Math", "English"}
threshold2 = 70.0

records3 = [
    ("A", "Math", 90),
    ("B", "English", 70)
]

required_subjects3 = set()
threshold3 = 80.0

def analyze_grades(
        records: list[tuple[str, str, int]],
        required_subjects: set[str],
        threshold: float
) -> tuple[dict[str, float], list[str]]:
    
    subject_averages = {}
    count = {}
    candidates = {}
    qualified_students = []

    for req_sub in required_subjects:
        subject_averages[req_sub] = 0
        count[req_sub] = 0

    for row in records:
        name, subject, score = row
        score = int(score)

        if name not in candidates:
            candidates[name] = {}

        if subject in required_subjects:
            subject_averages[subject] += score
            count[subject] += 1

            if score >= 60:
                candidates[name][subject] = score
                # candidates.setdefault(name, {})[subject] = score
                    # if name not in candidates:
                    # candidates[name] = []
                # candidates[name][subject] = score
    
    for subject in count:
        if count[subject] == 0:
            del subject_averages[subject]

    for req_sub in required_subjects:
        if count[req_sub] != 0:
            if subject_averages[req_sub] != 0:
                subject_averages[req_sub] = subject_averages[req_sub] / count[req_sub]

    for name, subject in candidates.items():
        if len(subject) == len(required_subjects):
            if sum(subject.values()) != 0:
                if sum((subject.values())) / len(required_subjects) >= threshold:
                    qualified_students.append(name)

    result = (subject_averages, qualified_students) 

    return result

print(analyze_grades(records, required_subjects, threshold))



def test_analyze_grades():
    assert analyze_grades(records, required_subjects, threshold) == (
    {
        "Math": 85.0,
        "English": 73.33333333333333
    },
    ["Alice", "Charlie"]
    )
    assert analyze_grades(records2, required_subjects2, threshold2) == (
    {
        "Math": 95.0,
        "English": 80.0
    },
    ["B"]
    )
    assert analyze_grades(records3, required_subjects3, threshold3) == ({}, [])
