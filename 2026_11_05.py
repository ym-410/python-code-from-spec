stock = {
    "apple": 10,
    "banana": 5
}

prices = {
    "apple": 100,
    "banana": 200
}

commands = [
    ("ADD", "apple", 3),
    ("ADD", "banana", 2),
    ("CHECKOUT",),
    ("ADD", "apple", 2),
    ("CHECKOUT",)
    ]

stock2 = {"apple": 3, "banana": 2}
prices2 = {"apple": 100, "banana": 200}

commands2 = [
    ("ADD", "apple", 4),
    ("ADD", "banana", 1),
    ("CHECKOUT",),
    ("REMOVE", "apple", 2),
    ("CHECKOUT",)
]

stock3 = {"apple": 5}
prices3 = {"apple": 100}

commands3 = [
    ("CHECKOUT",),
    ("REMOVE", "apple", 1),
    ("ADD", "apple", 2),
    ("REMOVE", "apple", 3)
]

def process_cart(
        stock: dict[str, int],
        prices: dict[str, int],
        commands: list[tuple]
) -> tuple[dict[str, int], dict[str, int], int, list[int]]:
    
    failure = []
    cart = {}
    total = 0
    now_stock = stock.copy()
    
    for i, command in enumerate(commands):
        handle = command[0]

        if handle == "ADD":
            item, quantity = command[-2:]
            
            if item not in now_stock or item not in prices:
                failure.append(i)
                continue
            
            if quantity < 1:
                failure.append(i)
                continue

            if item not in cart:
                cart[item] = quantity # カートに追加
            
            else:
                cart[item] += quantity


        elif handle == "REMOVE":
            item, quantity = command[-2:]

            if item not in cart:
                failure.append(i)
                
            elif quantity > cart[item]:
                failure.append(i)

            elif quantity == cart[item]:
                del cart[item]

            else:
                cart[item] -= quantity


        elif handle == "CHECKOUT":
            if len(cart) == 0:
                failure.append(i)

            if i not in failure:
                for cart_item, cart_quantity in cart.items():

                    if now_stock[cart_item] < cart_quantity:
                        failure.append(i)

            if i not in failure:
                for cart_item, cart_quantity in cart.items():
                    now_stock[cart_item] -= cart_quantity
                    total += prices[cart_item] * cart_quantity

                cart = {}

    return (now_stock, cart, total, failure)



def test_process_cart():
    assert process_cart(stock, prices, commands) == (
        {"apple": 5, "banana": 3},
        {},
        900,
        []
    )

    assert process_cart(stock2, prices2, commands2) == (
        {"apple": 1, "banana": 1},
        {},
        400,
        [2]
    )

    assert process_cart(stock3, prices3, commands3) == (
        {"apple": 5},
        {"apple": 2},
        0,
        [0, 1, 3]
    )






            
                
