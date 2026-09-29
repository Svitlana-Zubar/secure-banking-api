from fastapi import FastAPI
from app.routers.users import users_router
from app.routers.auth import auth_router

app = FastAPI(title="Secure Banking API")

@app.get("/")
def root():
    return {"message": "Secure Banking API is running"}

app.include_router(users_router)
app.include_router(auth_router)