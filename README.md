# 🏢 Sistem Manajemen Perusahaan HRD

Sistem manajemen perusahaan berbasis web ini dikembangkan menggunakan **Django** sebagai *framework backend* dan **MongoDB Atlas** sebagai *database* NoSQL utama, dihubungkan melalui *library* **MongoEngine**.

## Daftar Isi

1.  [Struktur Proyek](https://www.google.com/search?q=%231-struktur-proyek)
2.  [Teknologi](https://www.google.com/search?q=%232-teknologi)
3.  [Instalasi Lokal](https://www.google.com/search?q=%233-instalasi-lokal)
4.  [Konfigurasi Database](https://www.google.com/search?q=%234-konfigurasi-database)
5.  [Fitur Utama](https://www.google.com/search?q=%235-fitur-utama)
6.  [Deployment dengan Docker & Caddy](https://www.google.com/search?q=%236-deployment-dengan-docker--caddy)

-----

## 1\. Struktur Proyek

Struktur inti proyek ini mengikuti konvensi Django, dengan tambahan *file* konfigurasi Docker dan *environment variables*.

```
django-mongo-perusahaan/
├── PerusahaanKu/          # Direktori Pengaturan Proyek Django
│   ├── settings.py
│   └── urls.py
├── hrd/                   # Aplikasi HRD (Manajemen Karyawan)
│   ├── models.py          # Definisi Dokumen MongoEngine
│   ├── views.py           # Logika Bisnis (CRUD)
│   ├── urls.py
│   └── templates/
│       └── hrd/
│       └── registration/  # Template Login
├── .env                   # Environment Variables (Local)
├── Caddyfile              # Konfigurasi Reverse Proxy Caddy
├── Dockerfile             # Definisi Kontainer Aplikasi (Django/Gunicorn)
├── docker-compose.yml     # Definisi Multi-Kontainer (App, Caddy, DB)
├── manage.py
└── requirements.txt       # Dependencies Python
```

-----

## 2\. Teknologi

  * **Backend Framework:** Python 3.11, **Django**
  * **Database:** **MongoDB Atlas** (NoSQL)
  * **ODM:** **MongoEngine**
  * **Server WSGI:** **Gunicorn**
  * **Web Server/Reverse Proxy:** **Caddy** (untuk *deployment* Docker)
  * **Frontend:** HTML5, Bootstrap 5

-----

## 3\. Instalasi Lokal

Ikuti langkah-langkah ini untuk menjalankan proyek di lingkungan lokal Anda (tanpa Docker).

### A. Persiapan Lingkungan

```bash
# 1. Clone repositori
git clone https://github.com/IshikawaUta/erp-django-caddy-docker.git
cd django-mongo-perusahaan

# 2. Buat dan aktifkan virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# 3. Instal dependencies
pip install -r requirements.txt
```

### B. Setup Database Relasional Django

Django menggunakan database relasional (defaultnya SQLite) untuk sistem otentikasi (**Admin** dan **User**).

```bash
# Jalankan migrasi untuk membuat tabel bawaan (user, session, dll.)
python manage.py migrate
```

### C. Buat Akun Superuser

```bash
# Buat akun admin untuk mengakses sistem
python manage.py createsuperuser
```

### D. Jalankan Server

```bash
python manage.py runserver
```

Akses aplikasi di `http://127.0.0.1:8000/`.

-----

## 4\. Konfigurasi Database

### A. Koneksi MongoDB Atlas

Buat *file* **`.env`** di *root* proyek. Salin **Connection String (URI)** dari MongoDB Atlas Anda ke dalam *file* ini:

```env
# .env (digunakan oleh Django/Python)
MONGO_URI="mongodb+srv://<USERNAME>:<PASSWORD>@<CLUSTER_URL>/PerusahaanDB?retryWrites=true&w=majority"
```

Koneksi otomatis diinisiasi di `PerusahaanKu/settings.py` menggunakan *file* `.env` ini.

### B. Inisialisasi Data Awal

Aplikasi Anda membutuhkan data `Departemen` agar dapat menambahkan `Karyawan`.

1.  Akses URL inisialisasi: `http://127.0.0.1:8000/init_dept/`
2.  Ini akan menambahkan beberapa data `Departemen` contoh ke MongoDB Atlas Anda.

-----

## 5\. Fitur Utama

Sistem ini mendukung operasi **CRUD (Create, Read, Update, Delete)** penuh untuk data Karyawan.

| URL | View | Fungsionalitas |
| :--- | :--- | :--- |
| `/` | `daftar_karyawan` | Menampilkan semua data Karyawan. |
| `/tambah/` | `tambah_karyawan` | Menambahkan Karyawan baru. |
| `/departemen/tambah/` | `tambah_departemen` | Menambahkan entitas Departemen baru. |
| `/edit/<id>/` | `edit_karyawan` | Mengubah data Karyawan berdasarkan ID Mongo. |
| `/hapus/<id>/` | `hapus_karyawan` | Menghapus data Karyawan berdasarkan ID Mongo (membutuhkan POST). |

**Keamanan:** Semua *views* di atas dilindungi oleh decorator `@login_required`.

-----

## 6\. Deployment dengan Docker & Caddy

Proyek ini dikemas untuk *deployment* yang efisien menggunakan Docker Compose, Gunicorn, dan Caddy sebagai *reverse proxy* yang menangani *static files* dan *traffic* utama.

### A. Persiapan File Docker Compose

Pastikan Anda memiliki tiga *file* yang disiapkan dari panduan sebelumnya:

1.  **`Dockerfile`** (untuk *build* Gunicorn/App)
2.  **`Caddyfile`** (untuk *reverse proxy* dan *static files*)
3.  **`docker-compose.yml`** (orkestrasi semua layanan)

### B. Konfigurasi Database Docker Internal (Opsional)

Jika Anda ingin menjalankan *container* MongoDB *internal* (bukan MongoDB Atlas), buat *file* `.env` di *root* untuk Docker Compose (ini berbeda dengan `.env` Django):

```env
# .env (untuk Docker Compose)
MONGO_USER=docker_user
MONGO_PASSWORD=docker_pass
```

### C. Jalankan Deployment

Jalankan perintah berikut untuk membangun *image* dan menjalankan semua *service* dalam mode *detached* (`-d`):

```bash
docker compose up --build -d
```

### D. Akses dan Static Files

  * Aplikasi dapat diakses melalui `http://localhost/` atau `http://127.0.0.1/`.
  * Caddy secara otomatis menyajikan *static files* dari folder `staticfiles` yang dibuat selama *build* Docker.

### E. Menghentikan dan Membersihkan

Untuk menghentikan semua kontainer dan menghapus *volume* (termasuk data MongoDB):

```bash
# Menghentikan kontainer
docker compose down

# Menghentikan dan menghapus kontainer, jaringan, dan volume (data DB)
# HATI-HATI! Data akan hilang.
# docker compose down --volumes 
```