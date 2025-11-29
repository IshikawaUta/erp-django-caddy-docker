# hrd/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Karyawan, Departemen
from datetime import datetime
from bson.objectid import ObjectId
from django.contrib.auth.decorators import login_required

# View Daftar Karyawan
@login_required
def daftar_karyawan(request):
    # Mengambil semua dokumen Karyawan dan melakukan 'populate' (join) pada field departemen
    karyawan_list = Karyawan.objects.all().select_related()
    
    context = {
        'karyawan_list': karyawan_list
    }
    return render(request, 'hrd/daftar_karyawan.html', context)

# View Tambah Karyawan
@login_required
def tambah_karyawan(request):
    departemen_list = Departemen.objects.all()
    
    if request.method == 'POST':
        nama = request.POST.get('nama_lengkap')
        posisi = request.POST.get('posisi')
        tanggal_join = request.POST.get('tanggal_bergabung')
        status = request.POST.get('status')
        gaji = float(request.POST.get('gaji_pokok'))
        
        # Ambil objek Departemen berdasarkan ID yang dikirim dari form
        dept_id = request.POST.get('departemen')
        departemen_obj = Departemen.objects.get(id=dept_id)
        
        try:
            karyawan_baru = Karyawan(
                nama_lengkap=nama,
                posisi=posisi,
                departemen=departemen_obj,
                tanggal_bergabung=datetime.strptime(tanggal_join, '%Y-%m-%d'),
                status=status,
                gaji_pokok=gaji
            )
            karyawan_baru.save()
            return redirect('daftar_karyawan')
        except Exception as e:
            # Handle error (misal: data tidak valid)
            return render(request, 'hrd/tambah_karyawan.html', {'departemen_list': departemen_list, 'error': f"Gagal menyimpan: {e}"})

    return render(request, 'hrd/tambah_karyawan.html', {'departemen_list': departemen_list, 'status_choices': Karyawan.STATUS_CHOICES})

@login_required
def edit_karyawan(request, karyawan_id):
    # Cari objek Karyawan berdasarkan ID
    try:
        karyawan = Karyawan.objects.get(id=ObjectId(karyawan_id))
    except (Karyawan.DoesNotExist, Exception):
        # Tangani jika ID tidak ditemukan
        return redirect('daftar_karyawan')

    departemen_list = Departemen.objects.all()

    if request.method == 'POST':
        # Ambil data dari form
        nama = request.POST.get('nama_lengkap')
        posisi = request.POST.get('posisi')
        tanggal_join = request.POST.get('tanggal_bergabung')
        status = request.POST.get('status')
        gaji = float(request.POST.get('gaji_pokok'))
        dept_id = request.POST.get('departemen')
        
        # Ambil objek Departemen
        departemen_obj = Departemen.objects.get(id=dept_id)

        try:
            # Perbarui atribut objek Karyawan
            karyawan.nama_lengkap = nama
            karyawan.posisi = posisi
            karyawan.departemen = departemen_obj
            # Pastikan format tanggal benar
            karyawan.tanggal_bergabung = datetime.strptime(tanggal_join, '%Y-%m-%d')
            karyawan.status = status
            karyawan.gaji_pokok = gaji
            
            # Simpan perubahan ke MongoDB
            karyawan.save()
            return redirect('daftar_karyawan')
        except Exception as e:
            error_message = f"Gagal memperbarui data: {e}"
            return render(request, 'hrd/edit_karyawan.html', {
                'karyawan': karyawan, 
                'departemen_list': departemen_list, 
                'status_choices': Karyawan.STATUS_CHOICES,
                'error': error_message
            })

    # Jika method GET, tampilkan form edit
    context = {
        'karyawan': karyawan,
        'departemen_list': departemen_list,
        'status_choices': Karyawan.STATUS_CHOICES
    }
    return render(request, 'hrd/edit_karyawan.html', context)

# --------------------------
# --- FUNGSI HAPUS KARYAWAN ---
# --------------------------
@login_required
def hapus_karyawan(request, karyawan_id):
    # Cari objek Karyawan berdasarkan ID
    try:
        karyawan = Karyawan.objects.get(id=ObjectId(karyawan_id))
    except (Karyawan.DoesNotExist, Exception):
        return redirect('daftar_karyawan')

    # Hanya izinkan penghapusan via POST (praktik yang lebih aman)
    if request.method == 'POST':
        karyawan.delete()
        # Redirect kembali ke daftar karyawan
        return redirect('daftar_karyawan')
        
    # Jika diakses via GET, tampilkan halaman konfirmasi (Opsional, di sini kita langsung ke daftar)
    return redirect('daftar_karyawan')

# View Awal untuk membuat contoh data departemen
@login_required
def inisialisasi_departemen(request):
    if Departemen.objects.count() == 0:
        Departemen(nama="IT & Infrastruktur", lokasi="Lantai 5").save()
        Departemen(nama="Keuangan", lokasi="Lantai 3").save()
        Departemen(nama="Marketing", lokasi="Lantai 2").save()
        return redirect('daftar_karyawan')
    else:
        return redirect('daftar_karyawan')

@login_required
def tambah_departemen(request):
    """
    Menangani pembuatan dokumen Departemen baru di MongoDB Atlas.
    """
    if request.method == 'POST':
        nama_dept = request.POST.get('nama')
        lokasi_dept = request.POST.get('lokasi')
        
        try:
            # Membuat dan menyimpan dokumen Departemen baru
            departemen_baru = Departemen(nama=nama_dept, lokasi=lokasi_dept)
            departemen_baru.save()
            
            # Setelah berhasil, redirect kembali ke halaman tambah karyawan (atau daftar karyawan)
            return redirect('daftar_karyawan')
            
        except Exception as e:
            # Menangani error seperti nama departemen yang sudah ada (unique=True)
            error_message = f"Gagal menyimpan departemen. Pastikan Nama Departemen unik dan data valid. Error: {e}"
            return render(request, 'hrd/tambah_departemen.html', {'error': error_message})
            
    # Jika method GET, tampilkan formulir
    return render(request, 'hrd/tambah_departemen.html')