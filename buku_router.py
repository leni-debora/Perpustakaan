from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db.database import get_db
from schemas.buku_schema import BukuCreate, BukuUpdate, BukuResponse
from services.buku_service import BukuService

router = APIRouter(prefix="/api/buku", tags=["Buku"])

@router.get("/", response_model=List[BukuResponse])
def get_all_buku(db: Session = Depends(get_db)):
    return BukuService.get_all_buku(db)

@router.get("/search", response_model=List[BukuResponse])
def search_buku(
    judul: Optional[str] = Query(None),
    penulis: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    return BukuService.search_buku(db, judul, penulis)

@router.get("/{id_buku}", response_model=BukuResponse)
def get_buku_by_id(id_buku: int, db: Session = Depends(get_db)):
    return BukuService.get_buku_by_id(db, id_buku)

@router.post("/", response_model=BukuResponse)
def create_buku(buku: BukuCreate, db: Session = Depends(get_db)):
    return BukuService.create_buku(db, buku)

@router.put("/{id_buku}", response_model=BukuResponse)
def update_buku(id_buku: int, buku: BukuUpdate, db: Session = Depends(get_db)):
    return BukuService.update_buku(db, id_buku, buku)

@router.delete("/{id_buku}")
def delete_buku(id_buku: int, db: Session = Depends(get_db)):
    return BukuService.delete_buku(db, id_buku)