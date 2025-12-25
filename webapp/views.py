from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from .models import Item, Borrowing


def home(request):
    """Homepage dengan ringkasan statistik"""
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
    context = {
        'title': 'Daftar Barang',
        'items': items,
    }
    return render(request, 'items/list.html', context)


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
    
    context = {'title': 'Tambah Barang'}
    return render(request, 'items/add.html', context)


def item_detail(request, item_id):
    """Detail barang dan history peminjaman"""
    item = get_object_or_404(Item, id=item_id)
    borrowings = item.borrowings.all()
    
    context = {
        'title': f'Detail: {item.name}',
        'item': item,
        'borrowings': borrowings,
    }
    return render(request, 'items/detail.html', context)


def borrowings_list(request):
    """Daftar semua peminjaman aktif"""
    active_borrowings = Borrowing.objects.filter(is_returned=False)
    returned_borrowings = Borrowing.objects.filter(is_returned=True)
    
    context = {
        'title': 'Daftar Peminjaman',
        'active_borrowings': active_borrowings,
        'returned_borrowings': returned_borrowings,
    }
    return render(request, 'borrowings/list.html', context)


def borrow_item(request, item_id):
    """Form untuk meminjam barang"""
    item = get_object_or_404(Item, id=item_id)
    
    if request.method == 'POST':
        borrower_name = request.POST.get('borrower_name')
        quantity = int(request.POST.get('quantity', 1))
        notes = request.POST.get('notes', '')
        
        # Validasi ketersediaan
        if quantity > item.available:
            messages.error(request, f'Jumlah tidak mencukupi! Tersedia: {item.available}')
            return redirect('borrow_item', item_id=item.id)
        
        # Buat peminjaman
        borrowing = Borrowing.objects.create(
            item=item,
            borrower_name=borrower_name,
            quantity=quantity,
            notes=notes
        )
        
        # Update ketersediaan barang
        item.available -= quantity
        item.save()
        
        messages.success(request, f'Peminjaman berhasil dicatat! {borrower_name} meminjam {quantity} {item.name}')
        return redirect('borrowings_list')
    
    context = {
        'title': f'Pinjam: {item.name}',
        'item': item,
    }
    return render(request, 'borrowings/borrow.html', context)


def return_item(request, borrowing_id):
    """Mengembalikan barang yang dipinjam"""
    borrowing = get_object_or_404(Borrowing, id=borrowing_id)
    
    if not borrowing.is_returned:
        borrowing.return_item()
        messages.success(request, f'{borrowing.borrower_name} telah mengembalikan {borrowing.quantity} {borrowing.item.name}')
    else:
        messages.info(request, 'Barang sudah dikembalikan sebelumnya')
    
    return redirect('borrowings_list')

