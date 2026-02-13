from datetime import datetime, date, timedelta
from typing import List, Optional

class Buku:
    def __init__(self, id_buku: int, judul: str, penulis: str, tahun_terbit: int, isbn: str):
        self.id_buku = id_buku
        self.judul = judul
        self.penulis = penulis
        self.tahun_terbit = tahun_terbit
        self.isbn = isbn
        self.status = "tersedia"
    
    def update_status(self, status_baru: str):
        if status_baru in ["tersedia", "dipinjam"]:
            self.status = status_baru
    
    def get_info(self):
        return f"[{self.id_buku}] {self.judul} - {self.penulis} ({self.tahun_terbit}) - Status: {self.status}"

class Anggota:
    def __init__(self, id_anggota: int, nama: str, email: str, telepon: str):
        self.id_anggota = id_anggota
        self.nama = nama
        self.email = email
        self.telepon = telepon
        self.status = "aktif"
        self.tanggal_daftar = date.today()
    
    def cek_status(self):
        return self.status == "aktif"
    
    def get_info(self):
        return f"[{self.id_anggota}] {self.nama} - {self.email} - Status: {self.status}"

class Petugas:
    def __init__(self, id_petugas: int, nama: str, username: str, password: str):
        self.id_petugas = id_petugas
        self.nama = nama
        self.username = username
        self.password = password
    
    def get_info(self):
        return f"[{self.id_petugas}] {self.nama} - @{self.username}"

class Peminjaman:
    DENDA_PER_HARI = 1000
    
    def __init__(self, id_peminjaman: int, anggota: Anggota, buku: Buku, petugas: Petugas, durasi_hari: int = 7):
        self.id_peminjaman = id_peminjaman
        self.anggota = anggota
        self.buku = buku
        self.petugas = petugas
        self.tanggal_pinjam = date.today()
        self.tanggal_kembali = self.tanggal_pinjam + timedelta(days=durasi_hari)
        self.tanggal_pengembalian_aktual = None
        self.denda = 0
    
    def hitung_denda(self):
        if self.tanggal_pengembalian_aktual is None:
            hari_terlambat = (date.today() - self.tanggal_kembali).days
        else:
            hari_terlambat = (self.tanggal_pengembalian_aktual - self.tanggal_kembali).days
        
        if hari_terlambat > 0:
            self.denda = hari_terlambat * self.DENDA_PER_HARI
        else:
            self.denda = 0
        return self.denda
    
    def proses_pengembalian(self):
        self.tanggal_pengembalian_aktual = date.today()
        denda = self.hitung_denda()
        self.buku.update_status("tersedia")
        
        return {
            "id_peminjaman": self.id_peminjaman,
            "buku": self.buku.judul,
            "denda": denda,
            "status": "Terlambat" if denda > 0 else "Tepat waktu"
        }
    
    def get_info(self):
        status = "Dikembalikan" if self.tanggal_pengembalian_aktual else "Dipinjam"
        return f"[{self.id_peminjaman}] {self.anggota.nama} meminjam '{self.buku.judul}' | Pinjam: {self.tanggal_pinjam} | Kembali: {self.tanggal_kembali} | Status: {status} | Denda: Rp {self.denda:,.0f}"

class Perpustakaan:
    def __init__(self, nama: str):
        self.nama = nama
        self.daftar_buku = []
        self.daftar_anggota = []
        self.daftar_peminjaman = []
        self.daftar_petugas = []
        self._counter_buku = 1
        self._counter_anggota = 1
        self._counter_peminjaman = 1
        self._counter_petugas = 1
    
    def tambah_buku(self, judul: str, penulis: str, tahun_terbit: int, isbn: str):
        buku = Buku(self._counter_buku, judul, penulis, tahun_terbit, isbn)
        self.daftar_buku.append(buku)
        self._counter_buku += 1
        print(f"✓ Buku '{judul}' berhasil ditambahkan!")
        return buku
    
    def tambah_anggota(self, nama: str, email: str, telepon: str):
        anggota = Anggota(self._counter_anggota, nama, email, telepon)
        self.daftar_anggota.append(anggota)
        self._counter_anggota += 1
        print(f"✓ Anggota '{nama}' berhasil didaftarkan!")
        return anggota
    
    def tambah_petugas(self, nama: str, username: str, password: str):
        petugas = Petugas(self._counter_petugas, nama, username, password)
        self.daftar_petugas.append(petugas)
        self._counter_petugas += 1
        print(f"✓ Petugas '{nama}' berhasil ditambahkan!")
        return petugas
    
    def cari_buku(self, keyword: str = None, berdasarkan: str = "judul"):
        hasil = []
        keyword = keyword.lower() if keyword else ""
        
        for buku in self.daftar_buku:
            if berdasarkan == "judul" and keyword in buku.judul.lower():
                hasil.append(buku)
            elif berdasarkan == "penulis" and keyword in buku.penulis.lower():
                hasil.append(buku)
        
        return hasil
    
    def pinjam_buku(self, id_anggota: int, id_buku: int, id_petugas: int):
        anggota = next((a for a in self.daftar_anggota if a.id_anggota == id_anggota), None)
        if not anggota:
            print("✗ Anggota tidak ditemukan!")
            return None
        
        if not anggota.cek_status():
            print("✗ Anggota tidak aktif! Tidak dapat meminjam buku.")
            return None
        
        buku = next((b for b in self.daftar_buku if b.id_buku == id_buku), None)
        if not buku:
            print("✗ Buku tidak ditemukan!")
            return None
        
        if buku.status == "dipinjam":
            print("✗ Buku sedang dipinjam!")
            return None
        
        petugas = next((p for p in self.daftar_petugas if p.id_petugas == id_petugas), None)
        if not petugas:
            print("✗ Petugas tidak ditemukan!")
            return None
        
        peminjaman = Peminjaman(self._counter_peminjaman, anggota, buku, petugas)
        buku.update_status("dipinjam")
        self.daftar_peminjaman.append(peminjaman)
        self._counter_peminjaman += 1
        
        print(f"✓ Peminjaman berhasil!")
        print(f"  Buku: {buku.judul}")
        print(f"  Peminjam: {anggota.nama}")
        print(f"  Tanggal Kembali: {peminjaman.tanggal_kembali}")
        
        return peminjaman
    
    def kembalikan_buku(self, id_peminjaman: int):
        peminjaman = next((p for p in self.daftar_peminjaman if p.id_peminjaman == id_peminjaman), None)
        
        if not peminjaman:
            print("✗ Peminjaman tidak ditemukan!")
            return None
        
        if peminjaman.tanggal_pengembalian_aktual:
            print("✗ Buku sudah dikembalikan sebelumnya!")
            return None
        
        hasil = peminjaman.proses_pengembalian()
        
        print(f"✓ Pengembalian berhasil!")
        print(f"  Buku: {peminjaman.buku.judul}")
        print(f"  Status: {hasil['status']}")
        if hasil['denda'] > 0:
            print(f"  Denda: Rp {hasil['denda']:,.0f}")
        
        return hasil
    
    def tampilkan_daftar_buku(self):
        print(f"\n{'='*70}")
        print(f"DAFTAR BUKU - {self.nama}")
        print(f"{'='*70}")
        
        if not self.daftar_buku:
            print("Belum ada buku dalam perpustakaan.")
        else:
            for buku in self.daftar_buku:
                print(buku.get_info())
        
        print(f"{'='*70}\n")
    
    def tampilkan_riwayat_peminjaman(self):
        print(f"\n{'='*90}")
        print(f"RIWAYAT PEMINJAMAN - {self.nama}")
        print(f"{'='*90}")
        
        if not self.daftar_peminjaman:
            print("Belum ada riwayat peminjaman.")
        else:
            for peminjaman in self.daftar_peminjaman:
                print(peminjaman.get_info())
        
        print(f"{'='*90}\n")

def menu_utama():
    perpus = Perpustakaan("Cerdas Membaca")
    
    print("Inisialisasi data awal...")
    perpus.tambah_petugas("Admin Perpus", "admin", "admin123")
    perpus.tambah_buku("Python Programming", "John Doe", 2020, "978-1234567890")
    perpus.tambah_buku("Data Structures", "Jane Smith", 2019, "978-0987654321")
    perpus.tambah_anggota("Budi Santoso", "budi@email.com", "081234567890")
    
    while True:
        print("\n" + "="*50)
        print(f"SISTEM PERPUSTAKAAN '{perpus.nama}'")
        print("="*50)
        print("1. Tambah Buku")
        print("2. Tambah Anggota")
        print("3. Cari Buku")
        print("4. Pinjam Buku")
        print("5. Kembalikan Buku")
        print("6. Tampilkan Daftar Buku")
        print("7. Tampilkan Riwayat Peminjaman")
        print("0. Keluar")
        print("="*50)
        
        pilihan = input("Pilih menu: ")
        
        if pilihan == "1":
            print("\n--- Tambah Buku ---")
            judul = input("Judul: ")
            penulis = input("Penulis: ")
            tahun = int(input("Tahun Terbit: "))
            isbn = input("ISBN: ")
            perpus.tambah_buku(judul, penulis, tahun, isbn)
        
        elif pilihan == "2":
            print("\n--- Tambah Anggota ---")
            nama = input("Nama: ")
            email = input("Email: ")
            telepon = input("Telepon: ")
            perpus.tambah_anggota(nama, email, telepon)
        
        elif pilihan == "3":
            print("\n--- Cari Buku ---")
            print("1. Berdasarkan Judul")
            print("2. Berdasarkan Penulis")
            pilihan_cari = input("Pilih: ")
            keyword = input("Kata kunci: ")
            
            berdasarkan = "judul" if pilihan_cari == "1" else "penulis"
            hasil = perpus.cari_buku(keyword, berdasarkan)
            
            if hasil:
                print(f"\nDitemukan {len(hasil)} buku:")
                for buku in hasil:
                    print(buku.get_info())
            else:
                print("Tidak ada buku yang ditemukan.")
        
        elif pilihan == "4":
            print("\n--- Pinjam Buku ---")
            perpus.tampilkan_daftar_buku()
            id_anggota = int(input("ID Anggota: "))
            id_buku = int(input("ID Buku: "))
            id_petugas = int(input("ID Petugas: "))
            perpus.pinjam_buku(id_anggota, id_buku, id_petugas)
        
        elif pilihan == "5":
            print("\n--- Kembalikan Buku ---")
            perpus.tampilkan_riwayat_peminjaman()
            id_peminjaman = int(input("ID Peminjaman: "))
            perpus.kembalikan_buku(id_peminjaman)
        
        elif pilihan == "6":
            perpus.tampilkan_daftar_buku()
        
        elif pilihan == "7":
            perpus.tampilkan_riwayat_peminjaman()
        
        elif pilihan == "0":
            print("\nTerima kasih telah menggunakan sistem perpustakaan!")
            break
        
        else:
            print("Pilihan tidak valid!")

if __name__ == "__main__":
    menu_utama()