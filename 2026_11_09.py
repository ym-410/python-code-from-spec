def manage_config(
        defaults: dict[str, str | int | bool],
        commands: list[tuple]
) -> tuple[dict[str, str | int | bool], list[tuple]]:

    logs = []
    after_defaults = defaults.copy()

    for command in commands:

        handle = command[0]

        if handle == "SET":
            key, value = command[-2:]
            
            log = handle_set(key, value, after_defaults)
            logs.append(log)
        
        if handle == "DELETE":
            key = command[-1]

            log = handle_delete(key, after_defaults)
            
            if log:
                logs.append(log)

        if handle == "RESET":
            log = handle_reset(after_defaults, defaults)

            logs.append(log)
    
    results = (after_defaults, logs)
    return results

def handle_set(key, value, after_defaults):
    if key not in after_defaults:
        after_defaults[key] = value
        return ("SET", key, None, value)

    old_value = after_defaults[key]
    after_defaults[key] = value
    
    return ("SET", key, old_value, value)

def handle_delete(key, after_defaults):
    if key not in after_defaults:
        return None
    
    old_value = after_defaults[key]
    del after_defaults[key]

    return ("DELETE", key, old_value)

def handle_reset(after_defaults, defaults):
    previous_config = after_defaults.copy()

    after_defaults.clear()
    after_defaults.update(defaults)

    return ("RESET", previous_config)


# --- test ---

defaults1 = {
    "theme": "light",
    "volume": 50
}

commands1 = [
    ("SET", "theme", "dark"),
    ("SET", "volume", 80),
    ("RESET",),
    ("SET", "volume", 30)
]

defaults2: dict[str, str | int | bool] = {"mode": "normal"}

commands2 = [
    ("DELETE", "unknown"),
    ("SET", "mode", "fast"),
    ("DELETE", "mode")
]

defaults3: dict[str, str | int | bool] = {"debug": False}

commands3 = [
    ("SET", "cache", True),
    ("RESET",),
    ("RESET",)
]

defaults4 = {}

def test_manage_config():
    assert manage_config(defaults1, commands1) == (
            {"theme": "light", "volume": 30},

            [
                ("SET", "theme", "light", "dark"),
                ("SET", "volume", 50, 80),
                ("RESET", {"theme": "dark", "volume": 80}),
                ("SET", "volume", 50, 30)
            ]
    )

    assert manage_config(defaults2, commands2) == (
            {},
            [
                ("SET", "mode", "normal", "fast"),
                ("DELETE", "mode", "fast")
            ]
    )

    assert manage_config(defaults3, commands3) == (
            {"debug": False},
            [
                ("SET", "cache", None, True),
                ("RESET", {"debug": False, "cache": True}),
                ("RESET", {"debug": False})
            ]
    )


