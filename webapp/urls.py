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

