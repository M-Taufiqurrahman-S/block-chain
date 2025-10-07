import hashlib
import json
from time import time
from typing import List, Dict, Any
import os # Tambahkan import os untuk cek keberadaan file

BLOCKCHAIN_FILE = 'chain_data.json' 

class Block:
    """Representasi satu blok dalam rantai."""
    def __init__(self, index: int, timestamp: float, data: Dict[str, Any], previous_hash: str, proof: int = 0):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.proof = proof  # Untuk mekanisme Proof-of-Work (PoW) sederhana
        self.hash = self.calculate_hash()

    def calculate_hash(self) -> str:
        """Menghitung hash SHA-256 dari blok."""
        # Menghapus 'hash' agar tidak ikut di-hash saat pertama kali dihitung
        block_content = self.__dict__.copy()
        block_content.pop('hash', None)
        block_string = json.dumps(block_content, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

class Blockchain:
    """Kelas utama untuk mengelola rantai blok."""
    def __init__(self):
        self.chain: List[Dict[str, Any]] = []
        # Memanggil PoW saat membuat Genesis Block
        self.create_genesis_block()

    def save_chain(self):
        """Menyimpan rantai saat ini ke file JSON."""
        print(f"Saving blockchain to {BLOCKCHAIN_FILE}...")
        try:
            with open(BLOCKCHAIN_FILE, 'w') as f:
                json.dump(self.chain, f, indent=4)
        except Exception as e:
            print(f"Error saving chain: {e}")

    def load_chain(self) -> bool:
        """Memuat rantai dari file JSON jika ada."""
        if os.path.exists(BLOCKCHAIN_FILE):
            print(f"Loading blockchain from {BLOCKCHAIN_FILE}...")
            try:
                with open(BLOCKCHAIN_FILE, 'r') as f:
                    self.chain = json.load(f)
                return True
            except Exception as e:
                print(f"Error loading chain: {e}. Starting fresh.")
                return False
        return False
        

    def create_genesis_block(self):
        """Membuat blok pertama dalam rantai (Blok Genesis)."""
        genesis_block = Block(
            index=0,
            timestamp=time(),
            data={"message": "Genesis Block"},
            previous_hash="0"
        )
        self.chain.append(genesis_block.__dict__)

    def get_last_block(self) -> Dict[str, Any]:
        """Mengambil blok terakhir dalam rantai."""
        return self.chain[-1]

    def add_block(self, block: Block):
        """Menambahkan blok baru ke rantai."""
        # Memastikan hash sebelumnya cocok
        block.previous_hash = self.get_last_block()['hash']
        block.hash = block.calculate_hash()
        self.chain.append(block.__dict__)
        self.save_chain()

    def proof_of_work(self, last_proof: int) -> int:
        """Algoritma Proof of Work (PoW) sederhana."""
        proof = 0
        while self.is_valid_proof(last_proof, proof) is False:
            proof += 1
        return proof

    @staticmethod
    def is_valid_proof(last_proof: int, proof: int) -> bool:
        """Memvalidasi bukti: Apakah hash mengandung 4 angka nol di depan?"""
        guess = f'{last_proof}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def is_chain_valid(self) -> bool:
        """Memeriksa apakah seluruh rantai valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            # 1. Periksa Integritas Hash
            if current_block['previous_hash'] != previous_block['hash']:
                return False

            # 2. Periksa Validitas PoW
            if not self.is_valid_proof(previous_block['proof'], current_block['proof']):
                 return False

        return True

# Inisialisasi Blockchain global (HANYA untuk satu node/prototype)
blockchain_instance = Blockchain()