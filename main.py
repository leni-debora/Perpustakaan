from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db.database import engine, Base
from router import buku_router, anggota_router, peminjaman_router, petugas_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Perpustakaan Cerdas Membaca API",
    description="API untuk sistem manajemen perpustakaan",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(buku_router.router)
app.include_router(anggota_router.router)
app.include_router(peminjaman_router.router)
app.include_router(petugas_router.router)

@app.get("/")
def read_root():
    return {
        "message": "Selamat datang di API Perpustakaan Cerdas Membaca",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)