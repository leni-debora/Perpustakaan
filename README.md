# Soal 1: Implementasi OOP Python - Sistem Perpustakaan

## a) Fungsi Utama Sistem

1. Pencarian Buku - mencari berdasarkan judul atau penulis
2. Peminjaman Buku - anggota aktif dapat meminjam buku yang tersedia
3. Pengembalian Buku - proses pengembalian dengan perhitungan denda
4. Manajemen Status - tracking status anggota dan buku
5. Pencatatan Transaksi - semua transaksi dicatat oleh petugas
6. Perhitungan Denda - otomatis menghitung denda keterlambatan (Rp 1000/hari)

## b) Aktor yang Terlibat

1. Anggota Perpustakaan
   - Mencari buku
   - Meminjam buku (jika status aktif)
   - Mengembalikan buku
   - Membayar denda

2. Petugas/Staff Perpustakaan
   - Mencatat transaksi peminjaman
   - Mencatat transaksi pengembalian
   - Menghitung denda
   - Mengelola data buku dan anggota

## c) Entitas Kelas, Atribut, dan Method

### 1. Class Buku
Atribut:
- id_buku: int
- judul: str
- penulis: str
- tahun_terbit: int
- isbn: str
- status: str (tersedia/dipinjam)

Method:
- update_status(): mengubah status buku
- get_info(): menampilkan informasi buku

### 2. Class Anggota
Atribut:
- id_anggota: int
- nama: str
- email: str
- telepon: str
- status: str (aktif/non-aktif)
- tanggal_daftar: date

Method:
- cek_status(): mengecek status anggota
- get_info(): menampilkan informasi anggota

### 3. Class Peminjaman
Atribut:
- id_peminjaman: int
- anggota: Anggota
- buku: Buku
- tanggal_pinjam: date
- tanggal_kembali: date
- tanggal_pengembalian_aktual: date
- denda: float
- petugas: Petugas

Method:
- hitung_denda(): menghitung denda keterlambatan
- proses_pengembalian(): memproses pengembalian buku
- get_info(): menampilkan informasi peminjaman

### 4. Class Petugas
Atribut:
- id_petugas: int
- nama: str
- username: str
- password: str

Method:
- get_info(): menampilkan informasi petugas

### 5. Class Perpustakaan
Atribut:
- nama: str
- daftar_buku: list
- daftar_anggota: list
- daftar_peminjaman: list
- daftar_petugas: list

Method:
- tambah_buku(): menambah buku baru
- tambah_anggota(): menambah anggota baru
- cari_buku(): mencari buku
- pinjam_buku(): memproses peminjaman
- kembalikan_buku(): memproses pengembalian
- tampilkan_daftar_buku(): menampilkan semua buku
- tampilkan_riwayat_peminjaman(): menampilkan riwayat

## d) Cara Menjalankan

```bash
python perpustakaan.py
```

Program akan menampilkan menu interaktif untuk semua operasi perpustakaan.