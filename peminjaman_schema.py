from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class PeminjamanCreate(BaseModel):
    id_anggota: int = Field(..., gt=0)
    id_buku: int = Field(..., gt=0)
    id_petugas: int = Field(..., gt=0)
    durasi_hari: int = Field(default=7, ge=1, le=30)

class PeminjamanResponse(BaseModel):
    id_peminjaman: int
    id_anggota: int
    id_buku: int
    id_petugas: int
    tanggal_pinjam: date
    tanggal_kembali: date
    tanggal_pengembalian_aktual: Optional[date]
    denda: float
    
    class Config:
        from_attributes = True