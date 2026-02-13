from sqlalchemy.orm import Session
from models import Buku

class BukuRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Buku).all()
    
    @staticmethod
    def get_by_id(db: Session, id_buku: int):
        return db.query(Buku).filter(Buku.id_buku == id_buku).first()
    
    @staticmethod
    def search_by_judul(db: Session, judul: str):
        return db.query(Buku).filter(Buku.judul.ilike(f"%{judul}%")).all()
    
    @staticmethod
    def search_by_penulis(db: Session, penulis: str):
        return db.query(Buku).filter(Buku.penulis.ilike(f"%{penulis}%")).all()
    
    @staticmethod
    def create(db: Session, buku_data: dict):
        buku = Buku(**buku_data)
        db.add(buku)
        db.commit()
        db.refresh(buku)
        return buku
    
    @staticmethod
    def update(db: Session, id_buku: int, buku_data: dict):
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()
        if buku:
            for key, value in buku_data.items():
                if value is not None:
                    setattr(buku, key, value)
            db.commit()
            db.refresh(buku)
        return buku
    
    @staticmethod
    def delete(db: Session, id_buku: int):
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()
        if buku:
            db.delete(buku)
            db.commit()
            return True
        return False
    
    @staticmethod
    def update_status(db: Session, id_buku: int, status: str):
        buku = db.query(Buku).filter(Buku.id_buku == id_buku).first()
        if buku:
            buku.status = status
            db.commit()
            db.refresh(buku)
        return buku