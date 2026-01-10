from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from decimal import Decimal

from .models import Product, Cart, Order
from .forms import SignupForm


# ---------------- HOME ----------------
def home(request):
    return render(request, 'store/home.html')


# ---------------- PRODUCTS ----------------
def products(request):
    category = request.GET.get('category')
    products = Product.objects.filter(category=category) if category else Product.objects.all()
    return render(request, 'store/products.html', {'products': products})


def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product.html', {'product': product})


# ---------------- AUTH ----------------
def signup_view(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = SignupForm()
    return render(request, "store/signup.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect("home")
    else:
        form = AuthenticationForm()
    return render(request, "store/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


# ---------------- CART ----------------
@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    subtotal = sum(item.subtotal() for item in cart_items)
    discount = Decimal('0.00')
    coupon_code = None

    if request.method == "POST":
        coupon_code = request.POST.get('coupon')

        if coupon_code == "SAVE10":
            discount = subtotal * Decimal('0.10')
        elif coupon_code == "FESTIVE20":
            discount = subtotal * Decimal('0.20')
        else:
            messages.error(request, "Invalid coupon")

    gst = (subtotal - discount) * Decimal('0.05')
    delivery_fee = Decimal('50.00')
    grand_total = subtotal - discount + gst + delivery_fee

    return render(request, 'store/cart.html', {
        'cart_items': cart_items,
        'subtotal': subtotal,
        'discount': discount,
        'gst': gst,
        'delivery_fee': delivery_fee,
        'grand_total': grand_total,
        'coupon_code': coupon_code
    })


@login_required
def add_to_cart(request, product_id):
    if request.method != "POST":
        return redirect("products")

    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )

    if not created:
        cart_item.quantity += quantity
        cart_item.save()

    return redirect('cart')


@login_required
def increase_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    item.quantity += 1
    item.save()
    return redirect('cart')


@login_required
def decrease_qty(request, item_id):
    item = get_object_or_404(Cart, id=item_id, user=request.user)
    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()
    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    get_object_or_404(Cart, id=item_id, user=request.user).delete()
    return redirect('cart')


# ---------------- CHECKOUT ----------------
@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)
    cart_total = sum(item.subtotal() for item in cart_items)

    if request.method == "POST":
        Order.objects.create(
            user=request.user,
            total_amount=cart_total
        )
        cart_items.delete()
        return redirect('orders')


    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })


# ---------------- ORDERS ----------------
@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {'orders': orders})
    



@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'store/track_order.html', {'order': order})


# ---------------- SEARCH ----------------
def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query) |
        Q(category__icontains=query)
    ) if query else []

    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query
    })


# ---------------- CONTACT ----------------
def contact(request):
    if request.method == "POST":
        send_mail(
            subject=f"New Contact Message from {request.POST.get('name')}",
            message=request.POST.get('message'),
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],
        )
        return redirect("contact_success")
    return render(request, 'store/contact.html')


def contact_success(request):
    return render(request, "store/contact_success.html")


# ---------------- STATIC PAGES ----------------
def shipping_policy(request):
    return render(request, 'store/shipping_policy.html')


def return_refund_policy(request):
    return render(request, 'store/return_refund_policy.html')


def privacy_policy(request):
    return render(request, 'store/privacy_policy.html')


def terms_of_service(request):
    return render(request, 'store/terms_of_service.html')


def hamper_products(request):
    return render(request, 'store/hamper_products.html')
