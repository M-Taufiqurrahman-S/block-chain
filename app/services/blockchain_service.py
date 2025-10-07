# app/services/blockchain_service.py

import time
import hashlib
from typing import Dict, Any
from blockchain import blockchain_instance, Block
from app.models.schemas import TransactionInput # Import TransactionInput yang baru

# --- Helper Function: Hash Calculation ---
def calculate_transaction_hash(user_id: str, action: str, post_id: str) -> str:
    """
    Menghitung hash SHA-256 dari data transaksi penting.
    
    Dalam skenario nyata, ini akan me-hash data dari database (misal:
    username + photo_url + post_id). Di sini, kita simulasikan.
    """
    # Gabungkan data untuk di-hash
    data_to_hash = f"{user_id}:{action}:{post_id}:{time.time()}"
    return hashlib.sha256(data_to_hash.encode()).hexdigest()

# --- Blockchain Service Class ---
class BlockchainService:
    """Mengelola interaksi dengan objek blockchain_instance."""

    # ... (get_full_chain function tidak berubah)

    def mine_new_block(self, transaction: TransactionInput) -> Dict[str, Any]:
        """Melakukan Proof-of-Work dan menambahkan blok baru."""
        
        # 1. Hitung Hash Data di Backend (Baru!)
        # Kita gunakan post_id sebagai data kunci yang di-hash
        # Jika post_id tidak ada, gunakan user_id
        data_key = transaction.post_id if transaction.post_id else transaction.user_id
        
        # PENTING: Hash dihitung di sini, bukan diterima dari client
        data_hash = calculate_transaction_hash(
            user_id=transaction.user_id,
            action=transaction.action,
            post_id=data_key # Menggunakan data_key yang sudah dipastikan ada
        )

        last_block = blockchain_instance.get_last_block()
        last_proof = last_block['proof']
        
        # 2. Lakukan Proof-of-Work
        proof = blockchain_instance.proof_of_work(last_proof)

        # 3. Siapkan Data untuk Blok Baru
        block_data: Dict[str, Any] = {
            "user_id": transaction.user_id,
            "action": transaction.action,
            "data_hash": data_hash, # Gunakan hash yang dihitung di BE
            "original_id": data_key, # Simpan ID sumber sebagai konteks
            "timestamp_api": time.time()
        }

        # 4. Buat dan Tambahkan Blok Baru
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

# Inisialisasi service untuk digunakan di router
blockchain_service = BlockchainService()