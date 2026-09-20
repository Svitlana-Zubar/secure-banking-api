from fastapi import FastAPI

app = FastAPI(title="Secure Banking API")

@app.get("/")
def root():
    return {"message": "Secure Banking API is running"}