from django.shortcuts import render, get_object_or_404
from .models import Product, Category
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from rest_framework import viewsets
from .models import Product
from .serializers import ProductSerializer

class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

def product_list(request, category_slug=None):
    query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', 'name')

    categories = Category.objects.all()
    category = None

    products = Product.objects.filter(in_stock=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтрация по поисковому запросу
    if query.strip():
        products = products.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

    # Сортировка
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    else:
        products = products.order_by('name')

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'categories': categories,
        'category': category,
        'query': query,
        'sort_by': sort_by
    }

    return render(request, 'products/product_list.html', context)


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk, in_stock=True)
    return render(request, 'products/product_detail.html', {'product': product})