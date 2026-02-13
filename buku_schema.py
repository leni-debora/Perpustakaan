from pydantic import BaseModel, Field
from typing import Optional

class BukuBase(BaseModel):
    judul: str = Field(..., min_length=1, max_length=200)
    penulis: str = Field(..., min_length=1, max_length=100)
    tahun_terbit: int = Field(..., ge=1900, le=2100)
    isbn: str = Field(..., min_length=10, max_length=20)

class BukuCreate(BukuBase):
    pass

class BukuUpdate(BaseModel):
    judul: Optional[str] = Field(None, min_length=1, max_length=200)
    penulis: Optional[str] = Field(None, min_length=1, max_length=100)
    tahun_terbit: Optional[int] = Field(None, ge=1900, le=2100)
    isbn: Optional[str] = Field(None, min_length=10, max_length=20)
    status: Optional[str] = Field(None, pattern="^(tersedia|dipinjam)$")

class BukuResponse(BukuBase):
    id_buku: int
    status: str
    
    class Config:
        from_attributes = True