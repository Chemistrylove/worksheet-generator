from fpdf import FPDF
from fpdf.enums import XPos, YPos

from app.pdf.answer_formatting import format_answer


TITLE_MAP = {
    "linear_equation": "Linear Equations",
    "quadratic_equation": "Quadratic Equations",
    "system_of_linear_equations": "Systems of Linear Equations",
}


class WorksheetPDF(FPDF):
    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, self.title_text, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.set_font("Helvetica", "", 10)
        self.cell(0, 6, f"Difficulty: {self.difficulty_text.title()}", new_x=XPos.LMARGIN, new_y=YPos.NEXT, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 8)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


def _build_pdf(problems: list, question_type: str, difficulty: str, include_answers: bool) -> bytes:
    pdf = WorksheetPDF()
    pdf.title_text = TITLE_MAP.get(question_type, question_type)
    if include_answers:
        pdf.title_text += " - Answer Key"
    pdf.difficulty_text = difficulty

    pdf.add_page()

    for i, problem in enumerate(problems, start=1):
        pdf.set_font("Helvetica", "B", 12)
        pdf.multi_cell(
            0, 8, f"{i}. {problem['problem_text']}",
            new_x=XPos.LMARGIN, new_y=YPos.NEXT,
        )

        if include_answers:
            pdf.set_font("Helvetica", "I", 11)
            pdf.multi_cell(
                0, 8, f"Answer: {format_answer(problem)}",
                new_x=XPos.LMARGIN, new_y=YPos.NEXT,
            )
        else:
            pdf.ln(14)  # blank space for the student to work in

        pdf.ln(4)

    return bytes(pdf.output())


def build_worksheet_pdf(problems: list, question_type: str, difficulty: str) -> bytes:
    return _build_pdf(problems, question_type, difficulty, include_answers=False)


def build_answer_key_pdf(problems: list, question_type: str, difficulty: str) -> bytes:
    return _build_pdf(problems, question_type, difficulty, include_answers=True)