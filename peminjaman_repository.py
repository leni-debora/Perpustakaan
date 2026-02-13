from sqlalchemy.orm import Session
from models import Peminjaman
from datetime import date

class PeminjamanRepository:
    @staticmethod
    def get_all(db: Session):
        return db.query(Peminjaman).all()
    
    @staticmethod
    def get_by_id(db: Session, id_peminjaman: int):
        return db.query(Peminjaman).filter(Peminjaman.id_peminjaman == id_peminjaman).first()
    
    @staticmethod
    def get_by_anggota(db: Session, id_anggota: int):
        return db.query(Peminjaman).filter(Peminjaman.id_anggota == id_anggota).all()
    
    @staticmethod
    def get_aktif(db: Session):
        return db.query(Peminjaman).filter(Peminjaman.tanggal_pengembalian_aktual == None).all()
    
    @staticmethod
    def get_terlambat(db: Session):
        today = date.today()
        return db.query(Peminjaman).filter(
            Peminjaman.tanggal_pengembalian_aktual == None,
            Peminjaman.tanggal_kembali < today
        ).all()
    
    @staticmethod
    def create(db: Session, peminjaman_data: dict):
        peminjaman = Peminjaman(**peminjaman_data)
        db.add(peminjaman)
        db.commit()
        db.refresh(peminjaman)
        return peminjaman
    
    @staticmethod
    def update_pengembalian(db: Session, id_peminjaman: int, tanggal_pengembalian: date, denda: float):
        peminjaman = db.query(Peminjaman).filter(Peminjaman.id_peminjaman == id_peminjaman).first()
        if peminjaman:
            peminjaman.tanggal_pengembalian_aktual = tanggal_pengembalian
            peminjaman.denda = denda
            db.commit()
            db.refresh(peminjaman)
        return peminjaman   