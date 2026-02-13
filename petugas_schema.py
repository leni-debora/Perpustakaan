from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class PetugasBase(BaseModel):
    nama: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr

class PetugasCreate(PetugasBase):
    password: str = Field(..., min_length=6)

class PetugasUpdate(BaseModel):
    nama: Optional[str] = Field(None, min_length=1, max_length=100)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=6)

class PetugasResponse(PetugasBase):
    id_petugas: int
    
    class Config:
        from_attributes = True