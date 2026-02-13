from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from repository.petugas_repository import PetugasRepository
import hashlib

class PetugasService:
    @staticmethod
    def hash_password(password: str):
        return hashlib.sha256(password.encode()).hexdigest()
    
    @staticmethod
    def get_all_petugas(db: Session):
        return PetugasRepository.get_all(db)
    
    @staticmethod
    def get_petugas_by_id(db: Session, id_petugas: int):
        petugas = PetugasRepository.get_by_id(db, id_petugas)
        if not petugas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Petugas dengan ID {id_petugas} tidak ditemukan"
            )
        return petugas
    
    @staticmethod
    def create_petugas(db: Session, petugas_data):
        existing = PetugasRepository.get_by_username(db, petugas_data.username)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username sudah digunakan"
            )
        
        petugas_dict = petugas_data.dict()
        petugas_dict['password'] = PetugasService.hash_password(petugas_data.password)
        
        return PetugasRepository.create(db, petugas_dict)
    
    @staticmethod
    def update_petugas(db: Session, id_petugas: int, petugas_data):
        petugas = PetugasRepository.get_by_id(db, id_petugas)
        if not petugas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Petugas dengan ID {id_petugas} tidak ditemukan"
            )
        
        petugas_dict = petugas_data.dict(exclude_unset=True)
        
        if 'password' in petugas_dict and petugas_dict['password']:
            petugas_dict['password'] = PetugasService.hash_password(petugas_dict['password'])
        
        return PetugasRepository.update(db, id_petugas, petugas_dict)
    
    @staticmethod
    def delete_petugas(db: Session, id_petugas: int):
        petugas = PetugasRepository.get_by_id(db, id_petugas)
        if not petugas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Petugas dengan ID {id_petugas} tidak ditemukan"
            )
        
        PetugasRepository.delete(db, id_petugas)
        return {"message": "Petugas berhasil dihapus"}