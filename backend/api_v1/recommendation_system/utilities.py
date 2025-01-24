def make_hashable(d):
    return frozenset((k, tuple(v) if isinstance(v, list) else v) for k, v in d.items())
