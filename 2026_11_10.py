def process_orders(
        stock: dict[str, int],
        prices: dict[str, int],
        balances: dict[str, int],
        orders: list[tuple]
) -> tuple[dict[str, int], dict[str, int], list[tuple], list[int]]:
    
    now_stock = stock.copy()
    now_balances = balances.copy()
    logs = []
    fail = []

    for i, order in enumerate(orders):
        name, item, quantity = order

        # ユーザーが存在しない
        if name not in balances:
            fail.append(i)
        
        # 商品が在庫にない
        elif item not in stock:
            fail.append(i)
        
        # 商品が単価にない
        elif item not in prices:
            fail.append(i)

        # 要求個数が1未満
        elif quantity < 1:
            fail.append(i)

        # 在庫が要求個数未満
        elif now_stock[item] < quantity:
            fail.append(i)

        # ユーザーの残高不足
        elif now_balances[name] < prices[item] * quantity:
            fail.append(i)

        else:
            total = prices[item] * quantity
            now_balances[name] -= total
            now_stock[item] -= quantity
            logs.append((name, item, quantity, total))

    return (now_stock, now_balances, logs, fail)

        






# --- test ---

stock = {"apple": 5, "banana": 3}
prices = {"apple": 100, "banana": 200}
balances = {"Alice": 1000, "Bob": 300}

orders = [
        ("Alice", "apple", 3),
        ("Bob", "banana", 2),
        ("Bob", "apple", 2),
        ("Alice", "banana", 1)
]

stock2 = {"pen": 10}
prices2 = {"pen": 50}
balances2 = {"Alice": 200}

orders2 = [
    ("Bob", "pen", 1),
    ("Alice", "book", 1),
    ("Alice", "pen", 2)
]

stock3 = {"coffee": 2}
prices3 = {"coffee": 150}
balances3 = {"Alice": 300}

orders3 = [
    ("Alice", "coffee", 0),
    ("Alice", "coffee", 2),
    ("Alice", "coffee", 1)
]

def test_process_orders():
    assert process_orders(stock, prices, balances, orders) == (
            {"apple": 0, "banana": 2},
            {"Alice": 500, "Bob": 100},
            [
                ("Alice", "apple", 3, 300),
                ("Bob", "apple", 2, 200),
                ("Alice", "banana", 1, 200)
            ],
            [1]
    )

    assert process_orders(stock2, prices2, balances2, orders2) == (
    {"pen": 8},
    {"Alice": 100},
    [
        ("Alice", "pen", 2, 100)
    ],
    [0, 1]
    )

    assert process_orders(stock3, prices3, balances3, orders3) == (
    {"coffee": 0},
    {"Alice": 0},
    [
        ("Alice", "coffee", 2, 300)
    ],
    [0, 2]
    )
