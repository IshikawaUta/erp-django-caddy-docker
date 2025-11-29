# hrd/models.py
from mongoengine import Document, fields, CASCADE

# Model Departemen
class Departemen(Document):
    nama = fields.StringField(required=True, max_length=100, unique=True)
    lokasi = fields.StringField(max_length=100)
    
    meta = {'collection': 'departemen'} # Nama koleksi di MongoDB

    def __str__(self):
        return self.nama

# Model Karyawan
class Karyawan(Document):
    nama_lengkap = fields.StringField(required=True, max_length=150)
    posisi = fields.StringField(required=True, max_length=100)
    
    # ReferenceField: Menghubungkan Karyawan ke Departemen (seperti Foreign Key)
    # CASCADE: Jika Departemen dihapus, Karyawan yang terkait juga dihapus.
    departemen = fields.ReferenceField(Departemen, reverse_delete_rule=CASCADE) 
    
    tanggal_bergabung = fields.DateTimeField(required=True)
    
    STATUS_CHOICES = (
        ('Aktif', 'Aktif Bekerja'),
        ('Cuti', 'Cuti Panjang'),
        ('Resign', 'Sudah Keluar')
    )
    status = fields.StringField(choices=STATUS_CHOICES, default='Aktif')
    
    gaji_pokok = fields.FloatField(min_value=0.0)
    
    meta = {'collection': 'karyawan'} 

    def __str__(self):
        return self.nama_lengkap