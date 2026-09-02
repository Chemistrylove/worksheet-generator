from fastapi import FastAPI

app = FastAPI(title="Worksheet Generator API")


@app.get("/")
def read_root():
    return {"message": "Worksheet Generator API is running."}
    