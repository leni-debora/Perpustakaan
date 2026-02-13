from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date

class AnggotaBase(BaseModel):
    nama: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    telepon: str = Field(..., min_length=10, max_length=15)
    alamat: Optional[str] = Field(None, max_length=255)

class AnggotaCreate(AnggotaBase):
    pass

class AnggotaUpdate(BaseModel):
    nama: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    telepon: Optional[str] = Field(None, min_length=10, max_length=15)
    alamat: Optional[str] = Field(None, max_length=255)
    status: Optional[str] = Field(None, pattern="^(aktif|non-aktif)$")

class AnggotaResponse(AnggotaBase):
    id_anggota: int
    status: str
    tanggal_daftar: date
    
    class Config:
        from_attributes = True