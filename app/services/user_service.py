# app/services/user_service.py

import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import TransactionInput, User, UserCreate
from .blockchain_service import blockchain_service

# Dummy Database (menggantikan PostgreSQL/MySQL)
# Di aplikasi nyata, ini adalah koneksi ke DB.
_user_db: Dict[str, User] = {} 

class UserService:
    """Mengelola CRUD User dan integrasi opsional ke Blockchain."""

    def create_user(self, user_data: UserCreate) -> User:
        """Menambahkan User baru ke database dan mencatat transaksi ke Blockchain."""
        
        # 1. Simulasikan penyimpanan di Database
        user_id = str(uuid.uuid4()) # Generate ID unik
        new_user = User(
            id=user_id,
            name=user_data.name,
            email=user_data.email
            # Password disimpan (dan di-hash) tetapi tidak di model User output
        )
        _user_db[user_id] = new_user

        # 2. Opsional: Mencatat Transaksi Pendaftaran ke Blockchain
        # Kita panggil service blockchain di sini
        try:
            # Hash data penting: User ID + Email
            data_to_hash = f"{user_id}:{new_user.email}"
            
            # Kita panggil fungsi mine_new_block dengan TransactionInput
            blockchain_service.mine_new_block(
                transaction=TransactionInput(
                    user_id=user_id,
                    action="register",
                    post_id=user_id # Gunakan user_id sebagai ID kunci
                )
            )
            print(f"User {user_id} registered and transaction mined successfully.")
        except Exception as e:
            # Di aplikasi nyata, Anda mungkin perlu rollback atau log error
            print(f"Failed to mine block for new user: {e}")

        return new_user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Mengambil data user berdasarkan ID."""
        return _user_db.get(user_id)

    def get_all_users(self) -> List[User]:
        """Mengambil semua user."""
        return list(_user_db.values())

user_service = UserService()