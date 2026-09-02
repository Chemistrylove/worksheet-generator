# Worksheet Generator

A web app for tutors and teachers to generate math worksheets and answer keys as PDFs.

## MVP Scope

- Subject: Mathematics only
- Question types: Linear equations, Quadratic equations, Systems of linear equations
- Output: Printable worksheet PDF + separate answer key PDF
- All math problems and answers are generated and verified by Python — not by an LLM.

## Tech Stack

- Backend: Python + FastAPI
- Frontend: React + Vite (coming later)
- PDF generation: Python

## Running the backend locally

```bash
cd backend
source venv/bin/activate  # Windows: venv\Scripts\Activate.ps1
uvicorn app.main:app --reload