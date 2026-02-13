from sqlalchemy import Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.orm import relationship
from db.database import Base
from datetime import date

class Buku(Base):
    __tablename__ = "buku"
    
    id_buku = Column(Integer, primary_key=True, index=True, autoincrement=True)
    judul = Column(String(200), nullable=False)
    penulis = Column(String(100), nullable=False)
    tahun_terbit = Column(Integer, nullable=False)
    isbn = Column(String(20), unique=True, nullable=False)
    status = Column(String(20), default="tersedia")
    
    peminjaman = relationship("Peminjaman", back_populates="buku")

class Anggota(Base):
    __tablename__ = "anggota"
    
    id_anggota = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    telepon = Column(String(15), nullable=False)
    alamat = Column(String(255), nullable=True)
    status = Column(String(20), default="aktif")
    tanggal_daftar = Column(Date, default=date.today)
    
    peminjaman = relationship("Peminjaman", back_populates="anggota")

class Petugas(Base):
    __tablename__ = "petugas"
    
    id_petugas = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nama = Column(String(100), nullable=False)
    username = Column(String(50), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    peminjaman = relationship("Peminjaman", back_populates="petugas")

class Peminjaman(Base):
    __tablename__ = "peminjaman"
    
    id_peminjaman = Column(Integer, primary_key=True, index=True, autoincrement=True)
    id_anggota = Column(Integer, ForeignKey("anggota.id_anggota"), nullable=False)
    id_buku = Column(Integer, ForeignKey("buku.id_buku"), nullable=False)
    id_petugas = Column(Integer, ForeignKey("petugas.id_petugas"), nullable=False)
    tanggal_pinjam = Column(Date, nullable=False)
    tanggal_kembali = Column(Date, nullable=False)
    tanggal_pengembalian_aktual = Column(Date, nullable=True)
    denda = Column(Float, default=0)
    
    anggota = relationship("Anggota", back_populates="peminjaman")
    buku = relationship("Buku", back_populates="peminjaman")
    petugas = relationship("Petugas", back_populates="peminjaman")