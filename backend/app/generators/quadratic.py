import random


def generate_quadratic_equation(difficulty: str = "easy") -> dict:
    """
    Generates a quadratic equation of the form: a*x^2 + b*x + c = 0
    Built backwards from two known integer roots (r1, r2), so we
    always know the correct answers with certainty:
        a(x - r1)(x - r2) = 0
    Expanded: a*x^2 - a*(r1+r2)*x + a*r1*r2 = 0
    """
    if difficulty == "easy":
        a = 1
        r1 = random.randint(-8, 8)
        r2 = random.randint(-8, 8)
    elif difficulty == "medium":
        a = random.choice([1, 1, 1, 2])  # bias toward a=1, sometimes a=2
        r1 = random.randint(-10, 10)
        r2 = random.randint(-10, 10)
    elif difficulty == "hard":
        a = random.choice([1, 2, 3])
        r1 = random.randint(-12, 12)
        r2 = random.randint(-12, 12)
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    b = -a * (r1 + r2)
    c = a * r1 * r2

    roots = sorted([r1, r2])

    if not verify_quadratic_equation(a, b, c, roots):
        raise RuntimeError("Generated problem failed self-verification.")

    return {
        "type": "quadratic_equation",
        "difficulty": difficulty,
        "a": a,
        "b": b,
        "c": c,
        "problem_text": _format_equation(a, b, c),
        "answer": roots,
    }


def verify_quadratic_equation(a: int, b: int, c: int, claimed_roots: list) -> bool:
    """
    Independently re-solves a*x^2 + b*x + c = 0 using the quadratic formula
    and checks the results match the claimed roots (order-independent).
    """
    if a == 0:
        return False

    discriminant = b ** 2 - 4 * a * c
    if discriminant < 0:
        return False  # no real roots; shouldn't happen given how we build these

    sqrt_disc = discriminant ** 0.5
    root1 = (-b + sqrt_disc) / (2 * a)
    root2 = (-b - sqrt_disc) / (2 * a)

    solved = sorted([root1, root2])
    claimed = sorted(claimed_roots)

    return all(abs(s - cl) < 1e-6 for s, cl in zip(solved, claimed))


def _format_equation(a: int, b: int, c: int) -> str:
    a_part = f"{a}x²" if a != 1 else "x²"
    b_part = f"+ {b}x" if b > 0 else (f"- {abs(b)}x" if b < 0 else "")
    c_part = f"+ {c}" if c > 0 else (f"- {abs(c)}" if c < 0 else "")
    parts = [p for p in [a_part, b_part, c_part] if p]
    return " ".join(parts) + " = 0"