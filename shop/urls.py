from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('', views.product_all, name='product_all'),
    path('faqs/', views.faqs, name='faqs'),
    path('about/', views.about, name='about'),
    path('<slug:slug>', views.product_detail, name='product_detail'),
    path('shop/<slug:category_slug>/', views.category_list, name='category_list'),
]
