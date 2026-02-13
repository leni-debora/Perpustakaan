from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from datetime import date, timedelta
from repository.peminjaman_repository import PeminjamanRepository
from repository.buku_repository import BukuRepository
from repository.anggota_repository import AnggotaRepository
from repository.petugas_repository import PetugasRepository

class PeminjamanService:
    DENDA_PER_HARI = 1000
    
    @staticmethod
    def get_all_peminjaman(db: Session):
        return PeminjamanRepository.get_all(db)
    
    @staticmethod
    def get_peminjaman_by_id(db: Session, id_peminjaman: int):
        peminjaman = PeminjamanRepository.get_by_id(db, id_peminjaman)
        if not peminjaman:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Peminjaman dengan ID {id_peminjaman} tidak ditemukan"
            )
        return peminjaman
    
    @staticmethod
    def create_peminjaman(db: Session, peminjaman_data):
        anggota = AnggotaRepository.get_by_id(db, peminjaman_data.id_anggota)
        if not anggota:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anggota tidak ditemukan"
            )
        
        if anggota.status != "aktif":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Anggota tidak aktif! Tidak dapat meminjam buku."
            )
        
        buku = BukuRepository.get_by_id(db, peminjaman_data.id_buku)
        if not buku:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Buku tidak ditemukan"
            )
        
        if buku.status == "dipinjam":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Buku sedang dipinjam!"
            )
        
        petugas = PetugasRepository.get_by_id(db, peminjaman_data.id_petugas)
        if not petugas:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Petugas tidak ditemukan"
            )
        
        peminjaman_dict = {
            'id_anggota': peminjaman_data.id_anggota,
            'id_buku': peminjaman_data.id_buku,
            'id_petugas': peminjaman_data.id_petugas,
            'tanggal_pinjam': date.today(),
            'tanggal_kembali': date.today() + timedelta(days=peminjaman_data.durasi_hari),
            'denda': 0
        }
        
        peminjaman = PeminjamanRepository.create(db, peminjaman_dict)
        BukuRepository.update_status(db, peminjaman_data.id_buku, "dipinjam")
        
        return peminjaman
    
    @staticmethod
    def kembalikan_buku(db: Session, id_peminjaman: int):
        peminjaman = PeminjamanRepository.get_by_id(db, id_peminjaman)
        if not peminjaman:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Peminjaman dengan ID {id_peminjaman} tidak ditemukan"
            )
        
        if peminjaman.tanggal_pengembalian_aktual:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Buku sudah dikembalikan sebelumnya!"
            )
        
        tanggal_pengembalian = date.today()
        hari_terlambat = (tanggal_pengembalian - peminjaman.tanggal_kembali).days
        denda = 0
        
        if hari_terlambat > 0:
            denda = hari_terlambat * PeminjamanService.DENDA_PER_HARI
        
        PeminjamanRepository.update_pengembalian(db, id_peminjaman, tanggal_pengembalian, denda)
        BukuRepository.update_status(db, peminjaman.id_buku, "tersedia")
        
        return {
            "message": "Buku berhasil dikembalikan",
            "id_peminjaman": id_peminjaman,
            "tanggal_pengembalian": tanggal_pengembalian,
            "hari_terlambat": hari_terlambat if hari_terlambat > 0 else 0,
            "denda": denda,
            "status": "Terlambat" if denda > 0 else "Tepat waktu"
        }
    
    @staticmethod
    def get_peminjaman_aktif(db: Session):
        return PeminjamanRepository.get_aktif(db)
    
    @staticmethod
    def get_peminjaman_terlambat(db: Session):
        return PeminjamanRepository.get_terlambat(db)