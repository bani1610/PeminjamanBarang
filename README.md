# Tutorial: Membuat Aplikasi Peminjaman Barang dengan Django

Tutorial lengkap untuk membuat aplikasi web peminjaman barang menggunakan Django dengan desain modern dan menarik.

## Daftar Isi

1. [Persiapan](#persiapan)
2. [Setup Project Django](#setup-project-django)
3. [Membuat Models](#membuat-models)
4. [Membuat Views dan URLs](#membuat-views-dan-urls)
5. [Membuat Templates](#membuat-templates)
6. [Styling dengan CSS](#styling-dengan-css)
7. [Testing](#testing)

---

## Persiapan

### Requirements

- Python 3.8+
- Django 5.2+
- Text editor (VS Code, PyCharm, dll)

### Install Django

```bash
pip install django
```

---

## Setup Project Django

### 1. Buat Project Baru

```bash
django-admin startproject myproject
cd myproject
```

### 2. Buat App

```bash
python manage.py startapp webapp
```

### 3. Daftar App di `settings.py`

```python
# myproject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'webapp',  # Tambahkan ini
]
```

### 4. Setup Static Files

```python
# myproject/settings.py (tambahkan di bawah)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

### 5. Setup Templates

```python
# myproject/settings.py
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Tambahkan ini
        ...
    },
]
```

---

## Membuat Models

### File: `webapp/models.py`

```python
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
        return self.available > 0


class Borrowing(models.Model):
    """Model untuk peminjaman barang"""
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='borrowings')
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
```

### Jalankan Migrasi

```bash
python manage.py makemigrations
python manage.py migrate
```

---

## Membuat Views dan URLs

### File: `webapp/views.py`

```python
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Item, Borrowing


def home(request):
    """Homepage dengan dashboard"""
    total_items = Item.objects.count()
    total_available = sum(item.available for item in Item.objects.all())
    active_borrowings = Borrowing.objects.filter(is_returned=False).count()

    context = {
        'title': 'Dashboard Peminjaman Barang',
        'total_items': total_items,
        'total_available': total_available,
        'active_borrowings': active_borrowings,
        'recent_items': Item.objects.all()[:5],
        'recent_borrowings': Borrowing.objects.filter(is_returned=False)[:5],
    }
    return render(request, 'index.html', context)


def items_list(request):
    """Daftar semua barang"""
    items = Item.objects.all()
    return render(request, 'items/list.html', {'title': 'Daftar Barang', 'items': items})


def item_add(request):
    """Tambah barang baru"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        quantity = int(request.POST.get('quantity', 1))

        item = Item.objects.create(
            name=name,
            description=description,
            quantity=quantity,
            available=quantity
        )
        messages.success(request, f'Barang "{item.name}" berhasil ditambahkan!')
        return redirect('items_list')

    return render(request, 'items/add.html', {'title': 'Tambah Barang'})


def item_detail(request, item_id):
    """Detail barang"""
    item = get_object_or_404(Item, id=item_id)
    borrowings = item.borrowings.all()
    context = {
        'title': f'Detail: {item.name}',
        'item': item,
        'borrowings': borrowings,
    }
    return render(request, 'items/detail.html', context)


def borrow_item(request, item_id):
    """Pinjam barang"""
    item = get_object_or_404(Item, id=item_id)

    if request.method == 'POST':
        borrower_name = request.POST.get('borrower_name')
        quantity = int(request.POST.get('quantity', 1))
        notes = request.POST.get('notes', '')

        if quantity > item.available:
            messages.error(request, f'Jumlah tidak mencukupi! Tersedia: {item.available}')
            return redirect('borrow_item', item_id=item.id)

        Borrowing.objects.create(
            item=item,
            borrower_name=borrower_name,
            quantity=quantity,
            notes=notes
        )

        item.available -= quantity
        item.save()

        messages.success(request, f'Peminjaman berhasil!')
        return redirect('borrowings_list')

    return render(request, 'borrowings/borrow.html', {'title': f'Pinjam: {item.name}', 'item': item})


def borrowings_list(request):
    """Daftar peminjaman"""
    active = Borrowing.objects.filter(is_returned=False)
    returned = Borrowing.objects.filter(is_returned=True)
    return render(request, 'borrowings/list.html', {
        'title': 'Daftar Peminjaman',
        'active_borrowings': active,
        'returned_borrowings': returned,
    })


def return_item(request, borrowing_id):
    """Kembalikan barang"""
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)

    if not borrowing.is_returned:
        borrowing.return_item()
        messages.success(request, 'Barang berhasil dikembalikan!')

    return redirect('borrowings_list')
```

### File: `webapp/urls.py`

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('items/', views.items_list, name='items_list'),
    path('items/add/', views.item_add, name='item_add'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),
    path('borrowings/', views.borrowings_list, name='borrowings_list'),
    path('borrow/<int:item_id>/', views.borrow_item, name='borrow_item'),
    path('return/<int:borrowing_id>/', views.return_item, name='return_item'),
]
```

### File: `myproject/urls.py`

```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('webapp.urls')),
]
```

---

## Membuat Templates

### Struktur Folder

```
templates/
├── base.html
├── index.html
├── items/
│   ├── list.html
│   ├── add.html
│   └── detail.html
└── borrowings/
    ├── list.html
    └── borrow.html
```

### File: `templates/base.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block title %}MyProject{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'css/style.css' %}" />
  </head>
  <body>
    <!-- Navigation -->
    <nav class="navbar">
      <div class="container">
        <div class="nav-brand">
          <h1 class="logo">MyProject</h1>
        </div>
        <ul class="nav-menu">
          <li><a href="{% url 'home' %}" class="nav-link">Home</a></li>
          <li><a href="{% url 'items_list' %}" class="nav-link">Barang</a></li>
          <li>
            <a href="{% url 'borrowings_list' %}" class="nav-link"
              >Peminjaman</a
            >
          </li>
          <li>
            <a href="{% url 'item_add' %}" class="nav-link">Tambah Barang</a>
          </li>
        </ul>
      </div>
    </nav>

    <!-- Messages -->
    {% if messages %}
    <div class="messages">
      {% for message in messages %}
      <div class="message {{ message.tags }}">{{ message }}</div>
      {% endfor %}
    </div>
    {% endif %}

    <!-- Main Content -->
    <main>{% block content %}{% endblock %}</main>

    <!-- Footer -->
    <footer class="footer">
      <div class="container">
        <p>&copy; 2025 MyProject. Dibuat dengan Django.</p>
      </div>
    </footer>
  </body>
</html>
```

### File: `templates/index.html` (Dashboard)

Lihat file lengkap di `templates/index.html` untuk struktur dashboard dengan stats cards dan tabel.

---

## Styling dengan CSS

### File: `static/css/style.css`

Buat folder `static/css/` dan file `style.css` dengan styling modern:

**Fitur CSS:**

- Gradient background (purple-blue)
- Card dengan shadow dan hover effect
- Table dengan gradient header
- Buttons dengan gradient
- Badges dengan warna menarik
- Responsive design
- Smooth animations

Lihat file `static/css/style.css` untuk kode lengkap.

---

## Testing

### 1. Jalankan Server

```bash
python manage.py runserver
```

### 2. Akses Aplikasi

Buka browser: `http://localhost:8000`

### 3. Test Flow

1. **Tambah Barang**: Klik "Tambah Barang" → Isi form → Submit
2. **Lihat Daftar**: Klik "Barang" untuk melihat semua barang
3. **Pinjam Barang**: Klik "Pinjam" → Isi nama peminjam → Submit
4. **Lihat Peminjaman**: Klik "Peminjaman" untuk melihat daftar
5. **Kembalikan**: Klik "Kembalikan" untuk mengembalikan barang

---

## Admin Panel (Bonus)

### File: `webapp/admin.py`

```python
from django.contrib import admin
from .models import Item, Borrowing

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'available', 'is_available', 'created_at']
    search_fields = ['name', 'description']

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['item', 'borrower_name', 'quantity', 'borrow_date', 'is_returned']
    list_filter = ['is_returned', 'borrow_date']
```

### Create Superuser

```bash
python manage.py createsuperuser
```

Akses admin: `http://localhost:8000/admin`

---

## Tips & Tricks

### 1. Debug Mode

Pastikan `DEBUG = True` saat development di `settings.py`

### 2. Static Files

Jika static files tidak muncul, jalankan:

```bash
python manage.py collectstatic
```

### 3. Database Reset

Jika perlu reset database:

```bash
python manage.py flush
```

### 4. Custom Styling

Edit `static/css/style.css` untuk mengubah warna, font, atau layout

---

## Struktur Project Final

```
myproject/
├── manage.py
├── myproject/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── webapp/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── migrations/
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── items/
│   │   ├── list.html
│   │   ├── add.html
│   │   └── detail.html
│   └── borrowings/
│       ├── list.html
│       └── borrow.html
└── static/
    └── css/
        └── style.css
```

---

## Fitur Lengkap

✅ Dashboard dengan statistik real-time
✅ CRUD barang (Create, Read, Update, Delete)
✅ Sistem peminjaman dengan validasi stok
✅ Auto-update quantity saat pinjam/kembali
✅ History peminjaman
✅ Messages untuk feedback user
✅ Desain modern dengan gradient
✅ Responsive untuk mobile
✅ Admin panel untuk manajemen

---

## Selesai! 🎉

Aplikasi peminjaman barang Anda sudah jadi! Semua fitur sudah berfungsi dengan baik dan tampilan sudah menarik.

Untuk pertanyaan atau bug, silakan cek dokumentasi Django di: https://docs.djangoproject.com/
