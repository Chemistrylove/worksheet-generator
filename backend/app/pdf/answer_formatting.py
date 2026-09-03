def format_answer(problem: dict) -> str:
    """
    Converts a problem's answer (whatever shape it is) into a
    human-readable string for the answer key PDF.
    """
    problem_type = problem["type"]
    answer = problem["answer"]

    if problem_type == "linear_equation":
        return f"x = {answer}"

    elif problem_type == "quadratic_equation":
        roots = sorted(answer)
        if roots[0] == roots[1]:
            return f"x = {roots[0]}"
        return f"x = {roots[0]} or x = {roots[1]}"

    elif problem_type == "system_of_linear_equations":
        return f"x = {answer['x']}, y = {answer['y']}"

    else:
        raise ValueError(f"Unknown problem type: {problem_type}")