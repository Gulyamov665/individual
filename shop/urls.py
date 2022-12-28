from django.urls import path

from . import views

urlpatterns = [
    path('', views.products_list, name='products_list'),
    path('cart/', views.cart, name='cart'),
    path('delete_cart_item/<int:pk>', views.delete_cart_item, name='delete_cart_item'),
    path('edit_cart_item/<int:pk>', views.edit_cart_item, name='edit_cart_item'),
    path('product/<int:pk>', views.product_detail, name='product_detail'),
    path('cart/create_order', views.create_order, name='create_order'),
    path('orders/', views.orders, name='orders')

]
