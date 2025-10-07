from fastapi import FastAPI
# Import router dari folder app/api
from app.api.blockchain_router import router as blockchain_router

app = FastAPI(
    title="Blockchain API",
    description="A simple blockchain prototype built with FastAPI and Service Layer.",
    version="1.0.0"
)

# 1. Menambahkan Router/Controller ke aplikasi utama
# Semua endpoint sekarang akan dimulai dengan /blockchain (berdasarkan prefix di router.py)
app.include_router(blockchain_router)

# Endpoint root (opsional)
@app.get("/")
def read_root():
    return {"message": "Welcome to the Blockchain API. Access /docs for endpoints."}

# Anda sekarang menjalankan server dengan: uvicorn main:app --reload