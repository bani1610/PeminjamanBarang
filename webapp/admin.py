from django.contrib import admin
from .models import Item, Borrowing


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'quantity', 'available', 'is_available', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    

@admin.register(Borrowing)
class BorrowingAdmin(admin.ModelAdmin):
    list_display = ['item', 'borrower_name', 'quantity', 'borrow_date', 'is_returned', 'return_date']
    list_filter = ['is_returned', 'borrow_date', 'return_date']
    search_fields = ['borrower_name', 'item__name']
    readonly_fields = ['borrow_date', 'return_date']

