# hrd/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.daftar_karyawan, name='daftar_karyawan'),
    path('tambah/', views.tambah_karyawan, name='tambah_karyawan'),
    path('edit/<str:karyawan_id>/', views.edit_karyawan, name='edit_karyawan'),
    path('hapus/<str:karyawan_id>/', views.hapus_karyawan, name='hapus_karyawan'),
    path('departemen/tambah/', views.tambah_departemen, name='tambah_departemen'),
    path('init_dept/', views.inisialisasi_departemen, name='init_dept'),
]