from sqlalchemy.orm import Session
from typing import Optional
from fastapi import HTTPException, status
from repository.buku_repository import BukuRepository

class BukuService:
    @staticmethod
    def get_all_buku(db: Session):
        return BukuRepository.get_all(db)
    
    @staticmethod
    def get_buku_by_id(db: Session, id_buku: int):
        buku = BukuRepository.get_by_id(db, id_buku)
        if not buku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Buku dengan ID {id_buku} tidak ditemukan"
            )
        return buku
    
    @staticmethod
    def search_buku(db: Session, judul: Optional[str] = None, penulis: Optional[str] = None):
        if judul:
            return BukuRepository.search_by_judul(db, judul)
        elif penulis:
            return BukuRepository.search_by_penulis(db, penulis)
        else:
            return BukuRepository.get_all(db)
    
    @staticmethod
    def create_buku(db: Session, buku_data):
        buku_dict = buku_data.dict()
        buku_dict['status'] = 'tersedia'
        return BukuRepository.create(db, buku_dict)
    
    @staticmethod
    def update_buku(db: Session, id_buku: int, buku_data):
        buku = BukuRepository.get_by_id(db, id_buku)
        if not buku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Buku dengan ID {id_buku} tidak ditemukan"
            )
        
        buku_dict = buku_data.dict(exclude_unset=True)
        return BukuRepository.update(db, id_buku, buku_dict)
    
    @staticmethod
    def delete_buku(db: Session, id_buku: int):
        buku = BukuRepository.get_by_id(db, id_buku)
        if not buku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Buku dengan ID {id_buku} tidak ditemukan"
            )
        
        if buku.status == "dipinjam":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Tidak dapat menghapus buku yang sedang dipinjam"
            )
        
        BukuRepository.delete(db, id_buku)
        return {"message": "Buku berhasil dihapus"}