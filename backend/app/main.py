import io
import zipfile

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse

from app.generators.linear import generate_linear_equation
from app.generators.quadratic import generate_quadratic_equation
from app.generators.systems import generate_system_of_equations
from app.pdf.builder import build_worksheet_pdf, build_answer_key_pdf



from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Worksheet Generator API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


GENERATORS = {
    "linear_equation": generate_linear_equation,
    "quadratic_equation": generate_quadratic_equation,
    "system_of_linear_equations": generate_system_of_equations,
}

VALID_DIFFICULTIES = {"easy", "medium", "hard"}


def validate_and_get_generator(question_type: str, difficulty: str, count: int):
    """
    Shared validation for any endpoint that needs to generate problems.
    Raises HTTPException on bad input; returns the generator function to use.
    """
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

    return GENERATORS[question_type]


@app.get("/")
def read_root():
    return {"message": "Worksheet Generator API is running."}


@app.get("/generate")
def generate_problems(
    question_type: str,
    difficulty: str = "easy",
    count: int = 5,
):
    generator_fn = validate_and_get_generator(question_type, difficulty, count)
    problems = [generator_fn(difficulty) for _ in range(count)]

    return {
        "question_type": question_type,
        "difficulty": difficulty,
        "count": count,
        "problems": problems,
    }


@app.get("/worksheet")
def download_worksheet(
    question_type: str,
    difficulty: str = "easy",
    count: int = 5,
):
    generator_fn = validate_and_get_generator(question_type, difficulty, count)
    problems = [generator_fn(difficulty) for _ in range(count)]

    worksheet_bytes = build_worksheet_pdf(problems, question_type, difficulty)
    answer_key_bytes = build_answer_key_pdf(problems, question_type, difficulty)

    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zf:
        zf.writestr("worksheet.pdf", worksheet_bytes)
        zf.writestr("answer_key.pdf", answer_key_bytes)
    zip_buffer.seek(0)

    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={"Content-Disposition": "attachment; filename=worksheet_package.zip"},
    )