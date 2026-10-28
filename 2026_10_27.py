commands1 = [
        "IN apple 5",
        "IN banana 2",
        "OUT apple 3",
        "IN orange 4",
        "OUT banana 2"
]


commands2 = [
        "IN apple 3",
        "OUT apple 5",
        "OUT banana 1",
        "IN apple 2",
        "OUT apple 4"
]

commands3 = []



def process_inventory(commands: list[str]) -> tuple[dict[str, int], list[str]]:
    stock = {}
    error = []

    for row in commands:
        hand = row.split()[0]
        item = row.split()[1]
        pcs =  int(row.split()[2])
        
        if hand == "IN":
            if item not in stock:
                stock[item] = pcs
            else:
                stock[item] = stock.pop(item) + pcs
        
        if hand == "OUT":
            if item not in stock or stock.get(item, 0) < pcs:
                error.append(row)

            else:                
                stock[item] = stock.get(item, 0) - pcs

                if stock[item] == 0:
                    del stock[item]


    results = (stock, error)
    
    return results

print(process_inventory(commands1))
print(process_inventory(commands2))
print(process_inventory(commands3))


# アンパック代入
"""
hand, item, pcs = row.split()
>>> ["A", "B", "C"]
"""
