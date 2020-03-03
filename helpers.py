def stringify_dict(d, excluded_keys=[]):
    s = "-------------\n"
    for k, v in d.items():
        if k not in excluded_keys:
            s += f"{k}: {v}\n"

    s +="-------------\n"
    return s