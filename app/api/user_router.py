from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserCreate, User
from app.services.user_service import user_service
from typing import List

router = APIRouter(
    prefix="/users",  # Semua endpoint akan diawali /users
    tags=["User Management (CRUD)"]
)

# Endpoint: Create User (C - dari CRUD)
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user_endpoint(user_data: UserCreate):
    """Menambahkan user baru dan mencatat ke blockchain."""
    new_user = user_service.create_user(user_data)
    return new_user

# Endpoint: Read All Users (R - dari CRUD)
@router.get("/", response_model=List[User])
async def get_all_users_endpoint():
    """Mengambil semua data user."""
    return user_service.get_all_users()

# Endpoint: Read Single User (R - dari CRUD)
@router.get("/{user_id}", response_model=User)
async def get_user_endpoint(user_id: str):
    """Mengambil data user berdasarkan ID."""
    user = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Catatan: Anda bisa menambahkan PUT/DELETE di sini untuk Update/Delete