bookings = [
        (780, 840), # 13~14:00
        (600, 720), # 10~12:00
        (660, 780), # 11~13:00
        (900, 960)  # 15~16:00
]

window = (540, 1080) # 9~18:00

min_duration = 60


def find_free_slots(
        bookings: list[tuple[int, int]],
        window: tuple[int, int],
        min_duration: int
) -> list[tuple[int, int]]:

    win_start, win_end = window
    vacant = [[win_start, win_end]]
    checked_min_vacant = []

    for i in bookings:
        start, end = i
        next_vacant = []
                
        for j in vacant:
            win_start, win_end = j

            if end < win_start or win_end < start:
                next_vacant.append([win_start, win_end])
                continue

            if min(win_end, start) > win_start:
                next_vacant.append([win_start, min(win_end, start)])

            if win_end > max(win_start, end):
                next_vacant.append([max(win_start, end), win_end])
            
        vacant.clear()
        vacant.extend(next_vacant)

    for k in vacant:
        if k[1] - k[0] >= min_duration:
            checked_min_vacant.append(tuple(k))

    results = checked_min_vacant

    return results

print(find_free_slots(bookings, window, min_duration))

    

        




