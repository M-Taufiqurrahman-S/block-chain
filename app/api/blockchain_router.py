from fastapi import APIRouter, HTTPException, status
from app.models.schemas import TransactionInput
from app.services.blockchain_service import blockchain_service

# Inisialisasi APIRouter
router = APIRouter(
    prefix="/blockchain",  # Memberi prefix URL untuk semua endpoint di sini
    tags=["Blockchain Operations"]
)

# Endpoint GET /blockchain/chain
@router.get("/chain")
async def get_chain_endpoint():
    """Mengembalikan seluruh rantai blok."""
    # Controller hanya memanggil Service dan mengembalikan hasilnya
    return blockchain_service.get_full_chain()

# Endpoint POST /blockchain/mine
@router.post("/mine", status_code=status.HTTP_201_CREATED)
async def mine_block_endpoint(transaction: TransactionInput):
    """Menambang blok baru dan menambahkan data transaksi."""
    # Controller menerima input, memanggil Service, dan mengembalikan hasilnya
    return blockchain_service.mine_new_block(transaction)

# Endpoint GET /blockchain/validate
@router.get("/validate")
async def validate_chain_endpoint():
    """Memeriksa apakah rantai blockchain valid."""
    if blockchain_service.is_chain_valid():
        return {"message": "Chain is valid."}
    else:
        # Controller menangani respons HTTP Error
        raise HTTPException(status_code=400, detail="Chain is not valid!")