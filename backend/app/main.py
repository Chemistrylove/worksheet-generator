from fastapi import FastAPI, HTTPException

from app.generators.linear import generate_linear_equation
from app.generators.quadratic import generate_quadratic_equation
from app.generators.systems import generate_system_of_equations

app = FastAPI(title="Worksheet Generator API")

GENERATORS = {
    "linear_equation": generate_linear_equation,
    "quadratic_equation": generate_quadratic_equation,
    "system_of_linear_equations": generate_system_of_equations,
}

VALID_DIFFICULTIES = {"easy", "medium", "hard"}


@app.get("/")
def read_root():
    return {"message": "Worksheet Generator API is running."}


@app.get("/generate")
def generate_problems(
    question_type: str,
    difficulty: str = "easy",
    count: int = 5,
):
    if question_type not in GENERATORS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unknown question_type '{question_type}'. "
                f"Must be one of: {', '.join(GENERATORS.keys())}"
            ),
        )

    if difficulty not in VALID_DIFFICULTIES:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown difficulty '{difficulty}'. Must be one of: easy, medium, hard",
        )

    if not (1 <= count <= 50):
        raise HTTPException(
            status_code=400,
            detail="count must be between 1 and 50.",
        )

    generator_fn = GENERATORS[question_type]
    problems = [generator_fn(difficulty) for _ in range(count)]

    return {
        "question_type": question_type,
        "difficulty": difficulty,
        "count": count,
        "problems": problems,
    }