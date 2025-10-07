# app/services/user_service.py

import uuid
from typing import List, Dict, Any, Optional
from app.models.schemas import TransactionInput, User, UserCreate
from .blockchain_service import blockchain_service


_user_db: Dict[str, User] = {} 

class UserService:

    def create_user(self, user_data: UserCreate) -> User:
        
        user_id = str(uuid.uuid4()) 
        new_user = User(
            id=user_id,
            name=user_data.name,
            email=user_data.email
        )
        _user_db[user_id] = new_user

        try:
            data_to_hash = f"{user_id}:{new_user.email}"
            
            blockchain_service.mine_new_block(
                transaction=TransactionInput(
                    user_id=user_id,
                    action="register",
                    post_id=user_id
                )
            )
            print(f"User {user_id} registered and transaction mined successfully.")
        except Exception as e:
            print(f"Failed to mine block for new user: {e}")

        return new_user

    def get_user_by_id(self, user_id: str) -> Optional[User]:
        """Mengambil data user berdasarkan ID."""
        return _user_db.get(user_id)

    def get_all_users(self) -> List[User]:
        """Mengambil semua user."""
        return list(_user_db.values())

user_service = UserService()