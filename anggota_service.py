from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date
from repository.anggota_repository import AnggotaRepository

class AnggotaService:
    @staticmethod
    def get_all_anggota(db: Session):
        return AnggotaRepository.get_all(db)
    
    @staticmethod
    def get_anggota_by_id(db: Session, id_anggota: int):
        anggota = AnggotaRepository.get_by_id(db, id_anggota)
        if not anggota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anggota dengan ID {id_anggota} tidak ditemukan"
            )
        return anggota
    
    @staticmethod
    def create_anggota(db: Session, anggota_data):
        existing = AnggotaRepository.get_by_email(db, anggota_data.email)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email sudah terdaftar"
            )
        
        anggota_dict = anggota_data.dict()
        anggota_dict['status'] = 'aktif'
        anggota_dict['tanggal_daftar'] = date.today()
        return AnggotaRepository.create(db, anggota_dict)
    
    @staticmethod
    def update_anggota(db: Session, id_anggota: int, anggota_data):
        anggota = AnggotaRepository.get_by_id(db, id_anggota)
        if not anggota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anggota dengan ID {id_anggota} tidak ditemukan"
            )
        
        anggota_dict = anggota_data.dict(exclude_unset=True)
        return AnggotaRepository.update(db, id_anggota, anggota_dict)
    
    @staticmethod
    def delete_anggota(db: Session, id_anggota: int):
        anggota = AnggotaRepository.get_by_id(db, id_anggota)
        if not anggota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Anggota dengan ID {id_anggota} tidak ditemukan"
            )
        
        AnggotaRepository.delete(db, id_anggota)
        return {"message": "Anggota berhasil dihapus"}