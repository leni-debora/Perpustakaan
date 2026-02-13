from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.anggota_schema import AnggotaCreate, AnggotaUpdate, AnggotaResponse
from services.anggota_service import AnggotaService

router = APIRouter(prefix="/api/anggota", tags=["Anggota"])

@router.get("/", response_model=List[AnggotaResponse])
def get_all_anggota(db: Session = Depends(get_db)):
    return AnggotaService.get_all_anggota(db)

@router.get("/{id_anggota}", response_model=AnggotaResponse)
def get_anggota_by_id(id_anggota: int, db: Session = Depends(get_db)):
    return AnggotaService.get_anggota_by_id(db, id_anggota)

@router.post("/", response_model=AnggotaResponse)
def create_anggota(anggota: AnggotaCreate, db: Session = Depends(get_db)):
    return AnggotaService.create_anggota(db, anggota)

@router.put("/{id_anggota}", response_model=AnggotaResponse)
def update_anggota(id_anggota: int, anggota: AnggotaUpdate, db: Session = Depends(get_db)):
    return AnggotaService.update_anggota(db, id_anggota, anggota)

@router.delete("/{id_anggota}")
def delete_anggota(id_anggota: int, db: Session = Depends(get_db)):
    return AnggotaService.delete_anggota(db, id_anggota)