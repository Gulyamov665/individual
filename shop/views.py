from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from . import forms
from .forms import RateForm
from .models import Product, Slide, CardItem, Order, OrderProduct, Review


@login_required(login_url='/users/sign_in')
def products_list(request):
    search = request.GET.get('search')
    category = request.GET.get('category')
    brand = request.GET.get('brand')
    products = Product.objects.all()
    slides = Slide.objects.all()
    product_id = request.GET.get('product')
    if product_id:
        product = get_object_or_404(Product, pk=product_id)
        cart_item = CardItem.objects.filter(product=product, customer=request.user)
        if not cart_item:
            CardItem.objects.create(customer=request.user, product=product, quantity=1)
            return redirect('shop:products_list')
        for item in cart_item:
            item.quantity += 1
            item.save()
    products = products.filter(category=category) if category else products
    products = products.filter(brand=brand) if brand else products
    products = products.filter(Q(title__icontains=search) |
                               Q(description__icontains=search) |
                               Q(brand__name__icontains=search)) if search else products
    return render(request, 'products_list.html', {
        'products': products,
        'slides': slides
    })


def cart(request):
    cart_items = CardItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(request, 'cart.html', {
        'cart_item': cart_items,
        'total_quantity': total_quantity,
        'total_price': total_price
    })


def delete_cart_item(request, pk):
    cart_item = get_object_or_404(CardItem, pk=pk).delete()
    return redirect('shop:cart')


def edit_cart_item(request, pk):
    cart_item = get_object_or_404(CardItem, pk=pk)
    action = request.GET.get('action')
    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('shop:cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('shop:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('shop:cart')


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    reviews = Review.objects.filter(product=product)
    form = RateForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        instance = form.save(commit=False)
        instance.user = request.user
        instance.product = product
        instance.save()
        return redirect('shop:product_detail', pk=product.pk)
    return render(request, 'product_detail.html', {
        'product': product,
        'reviews': reviews,
        'form': form
    })


def create_order(request):
    cart_items = CardItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])

    form = forms.OrderForm(request.POST)
    if not cart_items:
        return render(request, 'error.html')

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            customer=request.user,
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price()
            )

        cart_items.delete()
        return redirect('shop:cart')

    return render(request, 'order_creation_page.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount,
        'form': form
    })


def orders(request):
    orders_list = Order.objects.filter(customer=request.user)
    return render(request, 'orders.html', {
        'orders': orders_list
    })
