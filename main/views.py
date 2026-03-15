from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product
from django.db.models import Q

# КАТАЛОГ
def index(request):
    """Страница каталога со всеми товарами и категориями + поиск"""
    categories = Category.objects.all()
    products = Product.objects.all()

    # ПОИСК
    query = request.GET.get('q')
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query)
        )

    return render(request, 'main/index.html', {
        'categories': categories,
        'products': products,
        'query': query
    })

# ГЛАВНАЯ
def about(request):
    """Главная страница с информацией о компании и популярными товарами"""
    popular_products = Product.objects.all().order_by('-id')[:4]
    return render(request, 'main/about.html', {
        'popular_products': popular_products
    })

# СТРАНИЦА ТОВАРА
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    analogs = product.get_analogs()


    return render(request, 'main/product_detail.html', {
        'product': product,
        'analogs': analogs,
    })

# СТРАНИЦА КАТЕГОРИИ
def category_detail(request, slug):
    """Страница с товарами конкретной категории"""
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'main/category_detail.html', {
        'category': category,
        'products': products
    })