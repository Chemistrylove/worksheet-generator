from app.generators.systems import generate_system_of_equations
from app.pdf.builder import build_worksheet_pdf, build_answer_key_pdf

problems = [generate_system_of_equations("easy") for _ in range(5)]

worksheet_bytes = build_worksheet_pdf(problems, "system_of_linear_equations", "easy")
answer_bytes = build_answer_key_pdf(problems, "system_of_linear_equations", "easy")

with open("test_worksheet.pdf", "wb") as f:
    f.write(worksheet_bytes)

with open("test_answer_key.pdf", "wb") as f:
    f.write(answer_bytes)

print("Done! Open test_worksheet.pdf and test_answer_key.pdf")