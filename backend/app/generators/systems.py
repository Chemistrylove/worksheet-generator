import random


def generate_system_of_equations(difficulty: str = "easy") -> dict:
    """
    Generates a system of two linear equations in x and y:
        a1*x + b1*y = c1
        a2*x + b2*y = c2
    Built backwards from a known integer solution (x, y), so we
    always know the correct answer with certainty.
    """
    if difficulty == "easy":
        coeff_range = (1, 8)
        sol_range = (-10, 10)
    elif difficulty == "medium":
        coeff_range = (-10, 10)
        sol_range = (-15, 15)
    elif difficulty == "hard":
        coeff_range = (-15, 15)
        sol_range = (-20, 20)
    else:
        raise ValueError(f"Unknown difficulty: {difficulty}")

    x = random.randint(*sol_range)
    y = random.randint(*sol_range)

    a1, b1, a2, b2 = _generate_independent_coefficients(coeff_range, difficulty)

    c1 = a1 * x + b1 * y
    c2 = a2 * x + b2 * y

    if not verify_system(a1, b1, c1, a2, b2, c2, x, y):
        raise RuntimeError("Generated problem failed self-verification.")

    return {
        "type": "system_of_linear_equations",
        "difficulty": difficulty,
        "a1": a1, "b1": b1, "c1": c1,
        "a2": a2, "b2": b2, "c2": c2,
        "problem_text": _format_system(a1, b1, c1, a2, b2, c2),
        "answer": {"x": x, "y": y},
    }


def _generate_independent_coefficients(coeff_range, difficulty, max_attempts=50):
    """
    Picks two equations' worth of coefficients and checks the determinant
    (a1*b2 - a2*b1) is nonzero, meaning the lines actually cross at one
    unique point rather than being parallel or identical.
    """
    low, high = coeff_range
    nonzero_choices = [i for i in range(low, high + 1) if i != 0]

    for _ in range(max_attempts):
        a1 = random.choice(nonzero_choices)
        b1 = random.choice(nonzero_choices)
        a2 = random.choice(nonzero_choices)
        b2 = random.choice(nonzero_choices)

        determinant = a1 * b2 - a2 * b1
        if determinant != 0:
            return a1, b1, a2, b2

    raise RuntimeError(
        "Could not generate independent equations after max attempts."
    )


def verify_system(a1, b1, c1, a2, b2, c2, claimed_x, claimed_y) -> bool:
    """
    Independently re-solves the system using Cramer's rule and checks
    the result matches the claimed (x, y).
    """
    determinant = a1 * b2 - a2 * b1
    if determinant == 0:
        return False  # no unique solution; shouldn't happen given our checks

    solved_x = (c1 * b2 - c2 * b1) / determinant
    solved_y = (a1 * c2 - a2 * c1) / determinant

    return (
        abs(solved_x - claimed_x) < 1e-9
        and abs(solved_y - claimed_y) < 1e-9
    )


def _format_system(a1, b1, c1, a2, b2, c2) -> str:
    return (
        f"{_format_line(a1, b1)} = {c1}\n"
        f"{_format_line(a2, b2)} = {c2}"
    )


def _format_line(a: int, b: int) -> str:
    a_part = f"{a}x" if a != 1 else "x"
    if a == -1:
        a_part = "-x"
    b_part = f"+ {b}y" if b >= 0 else f"- {abs(b)}y"
    return f"{a_part} {b_part}"