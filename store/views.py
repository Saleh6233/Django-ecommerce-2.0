from itertools import product

from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.cart import Cart
from django.http import JsonResponse
from django.db.models import Q


# Create your views here.


def store(request):
    sort = request.GET.get('sort', '')

    if sort == 'price_asc':
        products = Product.objects.all().order_by('price')
    elif sort == 'price_desc':
        products = Product.objects.all().order_by('-price')

    elif sort == 'title_asc':
        products = Product.objects.all().order_by('title')
    elif sort == 'title_desc':
        products = Product.objects.all().order_by('-title')
    elif sort == 'newest':
        products = Product.objects.all().order_by('-id')
    else:
        products = Product.objects.all()  # Default (no sorting)

    context = {'my_products': products}

    return render(request, 'store/store.html', context)


def categories(request):
    all_categories = Category.objects.all()

    return {'all_categories': all_categories}


def list_category(request, slug):
    category = get_object_or_404(Category, slug=slug)

    # Get price filter from GET parameters
    min_price = float(request.GET.get('min_price', 0))
    max_price = float(request.GET.get('max_price', 150.0))
    sort = request.GET.get('sort', '')

    try:
        min_price = int(min_price)
        max_price = int(max_price)
    except (ValueError, TypeError):
        min_price = 0
        max_price = 150

    # Filter products based on category and price range
    products = Product.objects.filter(
        category=category,
        price__gte=min_price,
        price__lte=max_price
    )

    sorting_options = {
        'newest': '-id',
        'price_asc': 'price',
        'price_desc': '-price',
        'title_asc': 'title',  # A-Z
        'title_desc': '-title',  # Z-A
    }

    order_by = sorting_options.get(sort, 'id')  # Default to newest
    products = products.order_by(order_by)

    context = {
        'category': category,
        'products': products,
        'current_min': min_price,
        'current_max': max_price
    }

    return render(request, 'store/list-category.html', context)


def product_info(request, slug):
    product_selected = get_object_or_404(Product, slug=slug)

    # # Initialize cart quantity to 0
    # cart_quantity = 0
    #
    # # Check if the product exists in the cart
    # if 'session_key' in request.session:
    #     cart = request.session.get('session_key')
    #     if cart and str(product_selected.id) in cart:
    #         cart_quantity = cart[str(product_selected.id)]['qty']
    #
    #
    #
    # # Calculate remaining stock
    # remaining_stock = product_selected.quantity - cart_quantity

    cart = Cart(request)
    product_id = str(product_selected.id)

    # Get quantity from cart or default to 0
    cart_quantity = cart.cart.get(product_id, {}).get('qty', 0)

    remaining_stock = product_selected.quantity - cart_quantity
    max_additional = max(remaining_stock, 0)  # Prevent negative values

    # print(type(remaining_stock))
    # print(remaining_stock)

    context = {
        'product': product_selected,
        'cart_quantity': cart_quantity,
        'remaining_stock': remaining_stock,
        'max_additional': max_additional  # How many more can be added
    }

    return render(request, 'store/product-info.html', context)


def search_products(request):
    """View to handle search queries and render search results page"""
    query = request.GET.get('q', '')

    if query:
        # Search in title, brand and description fields
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query) |
            Q(description__icontains=query)
        )
    else:
        products = Product.objects.none()

    context = {
        'query': query,
        'products': products,
        'product_count': products.count()
    }

    return render(request, 'store/search_results.html', context)


def ajax_search(request):
    """View to handle AJAX search queries and return JSON response"""
    query = request.GET.get('q', '')
    results = []

    if query:
        products = Product.objects.filter(
            Q(title__icontains=query) |
            Q(brand__icontains=query)
        )[:5]  # Limit to 5 results for the dropdown

        for product in products:
            results.append({
                'title': product.title,
                'slug': product.slug,
                'price': str(product.price),
                'image': product.image.url if product.image else '',
                'url': product.get_absolute_url(),  # Get the correct URL from the model
            })

    return JsonResponse({'results': results})
