class InvariantViolation(RuntimeError):
    pass


def enforce_invariant(condition: bool, msg: str):
    if not condition:
        raise InvariantViolation(msg)
