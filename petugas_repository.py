from sqlalchemy.orm import Session
from models import Petugas

class PetugasRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Petugas).all()
    
    @staticmethod
    def get_by_id(db: Session, id_petugas: int):
        return db.query(Petugas).filter(Petugas.id_petugas == id_petugas).first()
    
    @staticmethod
    def get_by_username(db: Session, username: str):
        return db.query(Petugas).filter(Petugas.username == username).first()
    
    @staticmethod
    def create(db: Session, petugas_data: dict):
        petugas = Petugas(**petugas_data)
        db.add(petugas)
        db.commit()
        db.refresh(petugas)
        return petugas
    
    @staticmethod
    def update(db: Session, id_petugas: int, petugas_data: dict):
        petugas = db.query(Petugas).filter(Petugas.id_petugas == id_petugas).first()
        if petugas:
            for key, value in petugas_data.items():
                if value is not None:
                    setattr(petugas, key, value)
            db.commit()
            db.refresh(petugas)
        return petugas
    
    @staticmethod
    def delete(db: Session, id_petugas: int):
        petugas = db.query(Petugas).filter(Petugas.id_petugas == id_petugas).first()
        if petugas:
            db.delete(petugas)
            db.commit()
            return True
        return False