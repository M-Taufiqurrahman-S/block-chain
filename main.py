from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from time import time
from typing import Dict, Any

# Import logika blockchain
from blockchain import Blockchain, Block, blockchain_instance

app = FastAPI()

# Pydantic Model untuk data yang diterima dari user
class TransactionData(BaseModel):
    user_id: str
    action: str  # e.g., "register", "post_photo"
    data_hash: str  # Hash dari data user/foto yang disimpan di database

@app.get("/chain")
async def get_chain():
    """Mengembalikan seluruh rantai blok."""
    return {
        "chain": blockchain_instance.chain,
        "length": len(blockchain_instance.chain),
        "crot_enak": "ngentot"
    }

@app.post("/mine")
async def mine_block(transaction: TransactionData):
    """Menambang blok baru dan menambahkan data transaksi."""
    last_block = blockchain_instance.get_last_block()
    last_proof = last_block['proof']
    
    # 1. Lakukan Proof-of-Work
    proof = blockchain_instance.proof_of_work(last_proof)

    # 2. Siapkan Data untuk Blok Baru
    block_data: Dict[str, Any] = {
        "user_id": transaction.user_id,
        "action": transaction.action,
        # Di sini kita hanya menyimpan hash data relasional dari DB (misal PostgreSQL)
        "data_hash": transaction.data_hash, 
        "timestamp_api": time()
    }

    # 3. Buat dan Tambahkan Blok Baru
    new_block = Block(
        index=len(blockchain_instance.chain),
        timestamp=time(),
        data=block_data,
        previous_hash="temp_hash", # placeholder, akan diperbarui di add_block
        proof=proof
    )

    blockchain_instance.add_block(new_block)

    return {
        "message": "New Block Mined",
        "block": new_block.__dict__
    }

@app.get("/validate")
async def validate_chain():
    """Memeriksa apakah rantai blockchain valid."""
    if blockchain_instance.is_chain_valid():
        return {"message": "Chain is valid."}
    else:
        raise HTTPException(status_code=400, detail="Chain is not valid!")