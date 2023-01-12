from django.urls import path
from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='remove'),
    path('update/<int:product_id>', views.cart_update, name='update'),
    path('delet/<int:product_id>', views.cart_delete, name='delete'),
    path('cart_add_not_form/<int:product_id>/',views.cart_add_not_form, name='add'),
]
