accounts1 = {
    "alice": 1000,
    "bob": 500,
    "charlie": 200
}

transactions1 = [
    ("DEPOSIT", "alice", 300),
    ("WITHDRAW", "bob", 200),
    ("TRANSFER", "alice", "charlie", 500),
    ("WITHDRAW", "bob", 400),
    ("TRANSFER", "charlie", "bob", 300)
]

accounts2 = {"A": 100, "B": 50}

transactions2 = [
    ("TRANSFER", "A", "C", 30),
    ("WITHDRAW", "B", 60),
    ("TRANSFER", "A", "B", 100),
    ("DEPOSIT", "C", 200)
]

accounts3 = {"A": 100}
transactions3 = []

def process_transactions(
        accounts: dict[str, int],
        transactions: list[tuple]
        ) -> tuple[dict[str, int], list[int]]:

    now_accounts = accounts.copy()
    fail = []
    
    for i, row in enumerate(transactions):
        process = row[0]
        account = row[1]
        amount = row[-1]

        if account not in accounts:
            fail.append(i)
            continue

        if process == "DEPOSIT":
            now_accounts[account] = now_accounts[account] + amount

        elif process == "WITHDRAW":
            if now_accounts[account] < amount:
                fail.append(i)
                continue
            else:
                now_accounts[account] = now_accounts[account] - amount

        elif process == "TRANSFER":
            destination = row[2]

            if destination not in now_accounts or destination == account:
                fail.append(i)
                continue

            if now_accounts[account] < amount:
                fail.append(i)
                continue

            else:
                now_accounts[destination] = now_accounts[destination] + amount
                now_accounts[account] -= amount


    result = (now_accounts, fail)

    return result 

def test_process_transactions():
    assert process_transactions(accounts1, transactions1) == (
            {
                "alice": 800,
                "bob": 600,
                "charlie": 400
            },
            [3]
    )

    assert process_transactions(accounts2, transactions2) == (
            (
                {"A": 0, "B": 150},
                [0, 1, 3]
            )
    )

    assert process_transactions(accounts3, transactions3) == (
            {"A": 100},
            []
    )
