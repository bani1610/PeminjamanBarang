from django.db import models
from django.utils import timezone


class Item(models.Model):
    """Model untuk barang yang bisa dipinjam"""
    name = models.CharField(max_length=200, verbose_name="Nama Barang")
    description = models.TextField(blank=True, verbose_name="Deskripsi")
    quantity = models.IntegerField(default=1, verbose_name="Jumlah Total")
    available = models.IntegerField(default=1, verbose_name="Jumlah Tersedia")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Tanggal Ditambahkan")
    
    class Meta:
        verbose_name = "Barang"
        verbose_name_plural = "Barang"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} ({self.available}/{self.quantity})"
    
    @property
    def is_available(self):
        """Cek apakah barang masih tersedia untuk dipinjam"""
        return self.available > 0


class Borrowing(models.Model):
    """Model untuk peminjaman barang"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrowings', verbose_name="Barang")
    borrower_name = models.CharField(max_length=200, verbose_name="Nama Peminjam")
    quantity = models.IntegerField(default=1, verbose_name="Jumlah Dipinjam")
    borrow_date = models.DateTimeField(default=timezone.now, verbose_name="Tanggal Peminjaman")
    return_date = models.DateTimeField(null=True, blank=True, verbose_name="Tanggal Pengembalian")
    is_returned = models.BooleanField(default=False, verbose_name="Sudah Dikembalikan")
    notes = models.TextField(blank=True, verbose_name="Catatan")
    
    class Meta:
        verbose_name = "Peminjaman"
        verbose_name_plural = "Peminjaman"
        ordering = ['-borrow_date']
    
    def __str__(self):
        status = "Dikembalikan" if self.is_returned else "Dipinjam"
        return f"{self.item.name} - {self.borrower_name} ({status})"
    
    def return_item(self):
        """Method untuk mengembalikan barang"""
        if not self.is_returned:
            self.is_returned = True
            self.return_date = timezone.now()
            self.item.available += self.quantity
            self.item.save()
            self.save()

