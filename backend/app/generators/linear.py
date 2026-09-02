import random


def generate_linear_equation(difficulty: str = "easy") -> dict:
    """
    Generates a linear equation of the form: a*x + b = c
    The equation is built backwards from a known integer solution (x),
    so we always know the correct answer with certainty.
    """
    if difficulty == "easy":
        a = random.randint(1, 10)
        x = random.randint(-10, 10)
        b = random.randint(-10, 10)
    elif difficulty == "medium":
        a = random.choice([i for i in range(-15, 16) if i != 0])
        x = random.randint(-20, 20)
        b = random.randint(-20, 20)
    elif difficulty == "hard":
        a = random.choice([i for i in range(-20, 21) if i != 0])
        x = random.randint(-30, 30)
        b = random.randint(-30, 30)
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    c = a * x + b

    if not verify_linear_equation(a, b, c, x):
        # Should never happen since we built it from x directly.
        # This is here as a safety net for when the logic above changes.
        raise RuntimeError("Generated problem failed self-verification.")

    return {
        "type": "linear_equation",
        "difficulty": difficulty,
        "a": a,
        "b": b,
        "c": c,
        "problem_text": _format_equation(a, b, c),
        "answer": x,
    }


def verify_linear_equation(a: int, b: int, c: int, claimed_answer) -> bool:
    """
    Independently re-solves a*x + b = c and checks it matches the claimed answer.
    This is intentionally separate from generation logic.
    """
    if a == 0:
        return False
    solved_x = (c - b) / a
    return abs(solved_x - claimed_answer) < 1e-9


def _format_equation(a: int, b: int, c: int) -> str:
    b_part = f"+ {b}" if b >= 0 else f"- {abs(b)}"
    return f"{a}x {b_part} = {c}"