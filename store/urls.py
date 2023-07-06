"""
URL configuration for my_store project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from store import views

urlpatterns = [
    path('', views.get_all_products, name='all_products'),
    path('product/<int:product_id>/', views.get_product_detail, name='product_detail'),
    path('game-consoles/', views.get_products_by_category, {'category_name': 'Game consoles'}, name='game_consoles'),
    path('gaming-laptops/', views.get_products_by_category, {'category_name': 'Gaming laptops'}, name='game_laptops'),
    path('gaming-pc/', views.get_products_by_category, {'category_name': 'Gaming PC'}, name='game_pc'),
    path('cart/', views.view_cart, name='cart'),
    path('add-item-to-cart/<int:pk>', views.add_item_to_cart, name='add_item_to_cart'),
    path('delete-item/<int:pk>', views.CartDeleteItem.as_view(), name='cart_delete_item'),
    path('make-order/', views.make_order, name='make_order'),
]
