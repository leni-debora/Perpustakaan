from sqlalchemy.orm import Session
from models import Anggota

class AnggotaRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Anggota).all()
    
    @staticmethod
    def get_by_id(db: Session, id_anggota: int):
        return db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str):
        return db.query(Anggota).filter(Anggota.email == email).first()
    
    @staticmethod
    def create(db: Session, anggota_data: dict):
        anggota = Anggota(**anggota_data)
        db.add(anggota)
        db.commit()
        db.refresh(anggota)
        return anggota
    
    @staticmethod
    def update(db: Session, id_anggota: int, anggota_data: dict):
        anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
        if anggota:
            for key, value in anggota_data.items():
                if value is not None:
                    setattr(anggota, key, value)
            db.commit()
            db.refresh(anggota)
        return anggota
    
    @staticmethod
    def delete(db: Session, id_anggota: int):
        anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
        if anggota:
            db.delete(anggota)
            db.commit()
            return True
        return False
    
    @staticmethod
    def check_status(db: Session, id_anggota: int):
        anggota = db.query(Anggota).filter(Anggota.id_anggota == id_anggota).first()
        return anggota.status == "aktif" if anggota else False