from fastapi import FastAPI
from app.routers.users import router

app = FastAPI(title="Secure Banking API")

@app.get("/")
def root():
    return {"message": "Secure Banking API is running"}

app.include_router(router)