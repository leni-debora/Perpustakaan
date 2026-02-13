from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.peminjaman_schema import PeminjamanCreate, PeminjamanResponse
from services.peminjaman_service import PeminjamanService

router = APIRouter(prefix="/api/peminjaman", tags=["Peminjaman"])

@router.get("/", response_model=List[PeminjamanResponse])
def get_all_peminjaman(db: Session = Depends(get_db)):
    return PeminjamanService.get_all_peminjaman(db)

@router.get("/aktif", response_model=List[PeminjamanResponse])
def get_peminjaman_aktif(db: Session = Depends(get_db)):
    return PeminjamanService.get_peminjaman_aktif(db)

@router.get("/terlambat", response_model=List[PeminjamanResponse])
def get_peminjaman_terlambat(db: Session = Depends(get_db)):
    return PeminjamanService.get_peminjaman_terlambat(db)

@router.get("/{id_peminjaman}", response_model=PeminjamanResponse)
def get_peminjaman_by_id(id_peminjaman: int, db: Session = Depends(get_db)):
    return PeminjamanService.get_peminjaman_by_id(db, id_peminjaman)

@router.post("/", response_model=PeminjamanResponse)
def pinjam_buku(peminjaman: PeminjamanCreate, db: Session = Depends(get_db)):
    return PeminjamanService.create_peminjaman(db, peminjaman)

@router.put("/{id_peminjaman}/kembalikan")
def kembalikan_buku(id_peminjaman: int, db: Session = Depends(get_db)):
    return PeminjamanService.kembalikan_buku(db, id_peminjaman)