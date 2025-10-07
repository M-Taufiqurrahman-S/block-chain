import time
import hashlib
from typing import Dict, Any
from blockchain import blockchain_instance, Block
from app.models.schemas import TransactionInput 

def calculate_transaction_hash(user_id: str, action: str, post_id: str) -> str:
  
    data_to_hash = f"{user_id}:{action}:{post_id}:{time.time()}"
    return hashlib.sha256(data_to_hash.encode()).hexdigest()

class BlockchainService:

    def get_full_chain(self) -> Dict[str, Any]:
        return {
            "chain": blockchain_instance.chain,
            "length": len(blockchain_instance.chain)
        }

    def mine_new_block(self, transaction: TransactionInput) -> Dict[str, Any]:
        data_key = transaction.post_id if transaction.post_id else transaction.user_id
        
        data_hash = calculate_transaction_hash(
            user_id=transaction.user_id,
            action=transaction.action,
            post_id=data_key 
        )

        last_block = blockchain_instance.get_last_block()
        last_proof = last_block['proof']
        
        proof = blockchain_instance.proof_of_work(last_proof)

        block_data: Dict[str, Any] = {
            "user_id": transaction.user_id,
            "action": transaction.action,
            "data_hash": data_hash, 
            "original_id": data_key, 
            "timestamp_api": time.time()
        }

        new_block = Block(
            index=len(blockchain_instance.chain),
            timestamp=time.time(),
            data=block_data,
            previous_hash="temp_hash", 
            proof=proof
        )

        blockchain_instance.add_block(new_block)

        return {
            "message": "New Block Mined",
            "block": new_block.__dict__
        }
    def is_chain_valid(self) -> bool:
        """Memvalidasi integritas rantai."""
        return blockchain_instance.is_chain_valid()

blockchain_service = BlockchainService()