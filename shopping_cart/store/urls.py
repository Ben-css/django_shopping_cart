from django.urls import path, include
from . import views

urlpatterns = [
    path('accounts/login/',views.login, name='login'),
    path('accounts/logout/',views.logout, name='logout'),
    path('index/',views.index,name='index'),
    path('cart/',views.cart,name='cart'),
    path('add_to_cart/',views.add_to_cart,name='add_to_cart'),
    path('accounts/register/', views.register,name='register'),
]
