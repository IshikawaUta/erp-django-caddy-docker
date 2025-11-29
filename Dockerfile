# Dockerfile

# Menggunakan Python base image
FROM python:3.11-slim

# Mengatur environment variable
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE PerusahaanKu.settings

# Membuat dan mengatur direktori kerja
WORKDIR /app

# Menyalin requirements dan menginstall dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Menyalin kode proyek
COPY . /app/

# Mengumpulkan static files (PENTING untuk admin/bootstrap)
# Pastikan Anda telah mengonfigurasi STATIC_ROOT di settings.py
# Contoh: STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
RUN python manage.py collectstatic --noinput

# Menggunakan Gunicorn untuk menjalankan aplikasi
# Bind ke 0.0.0.0:8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "PerusahaanKu.wsgi:application"]