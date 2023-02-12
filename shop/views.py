from django.shortcuts import render, get_object_or_404
from .models import Category, Product


def product_all(request):
    products = Product.objects.prefetch_related('product_image').filter(is_active=True)
    return render(request, 'home.html', {'products': products})


def faqs(request):
    return render(request, 'faqs.html')


def about(request):
    return render(request, 'about.html')


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    return render(request, 'products/details.html', {'product': product})


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(name=category_slug).get_descendants(include_self=True)
    )
    return render(request, 'products/category.html', {'category': category, 'products': products})
