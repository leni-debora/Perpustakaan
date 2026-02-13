from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from db.database import get_db
from schemas.petugas_schema import PetugasCreate, PetugasUpdate, PetugasResponse
from services.petugas_service import PetugasService

router = APIRouter(prefix="/api/petugas", tags=["Petugas"])

@router.get("/", response_model=List[PetugasResponse])
def get_all_petugas(db: Session = Depends(get_db)):
    return PetugasService.get_all_petugas(db)

@router.get("/{id_petugas}", response_model=PetugasResponse)
def get_petugas_by_id(id_petugas: int, db: Session = Depends(get_db)):
    return PetugasService.get_petugas_by_id(db, id_petugas)

@router.post("/", response_model=PetugasResponse)
def create_petugas(petugas: PetugasCreate, db: Session = Depends(get_db)):
    return PetugasService.create_petugas(db, petugas)

@router.put("/{id_petugas}", response_model=PetugasResponse)
def update_petugas(id_petugas: int, petugas: PetugasUpdate, db: Session = Depends(get_db)):
    return PetugasService.update_petugas(db, id_petugas, petugas)

@router.delete("/{id_petugas}")
def delete_petugas(id_petugas: int, db: Session = Depends(get_db)):
    return PetugasService.delete_petugas(db, id_petugas)