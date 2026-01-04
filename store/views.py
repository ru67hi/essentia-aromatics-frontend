from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Product, Cart, Order
from decimal import Decimal
from django.db.models import Q





def home(request):
    return render(request, 'store/home.html')

def products(request):
    category = request.GET.get('category')

    if category:
        products = Product.objects.filter(category=category)
    else:
        products = Product.objects.all()

    return render(request, 'store/products.html', {'products': products})

def product(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'store/product.html', {'product': product})

def cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    return render(request, 'store/cart.html', {'cart_items': cart_items})

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    quantity = int(request.POST.get('quantity', 1))

    cart_item, created = Cart.objects.get_or_create(
        user=request.user,
        product=product,
        defaults={'quantity': quantity}
    )
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


def cart(request):
    return render(request, 'store/cart.html')



def login_view(request):
    return render(request, 'store/login.html')




def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')   # or 'login' or 'home'
    else:
        form = SignupForm()

    return render(request, 'store/signup.html', {'form': form})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        send_mail(
            subject=f"New Contact Message from {name}",
            message=f"Sender Email: {email}\n\nMessage:\n{message}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.EMAIL_HOST_USER],  # REGISTERED MAIL
            fail_silently=False,
        )
        return redirect("contact_success")
    return render(request, 'store/contact.html')


def contact_success(request):
    return render(request, "contact_success.html")

def combos(request):
    products = Product.objects.filter(category='combo')
    return render(request, 'store/combos.html', {'products': products})
    


def combo_products(request):
    products = Product.objects.filter(category='combo')
    return render(request, 'store/combo_products.html', {
        'products': products
    })



def hamper_products(request):
    products = Product.objects.filter(category='hamper')
    return render(request, 'store/hamper_products.html', {
        'products': products
    })




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

    gst = (subtotal - discount) * Decimal('0.5')
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
def increase_qty(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')


@login_required
def decrease_qty(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)

    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()

    return redirect('cart')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(Cart, id=item_id, user=request.user)
    cart_item.delete()
    return redirect('cart')







def apply_coupon(request):
    if request.method == 'POST':
        code = request.POST.get('coupon')

        # Coupon logic
        if code == 'SAVE10':
            request.session['discount'] = 10
            messages.success(request, 'FIRST10 applied! 10% discount added.')

        elif code == 'FESTIVE20':
            request.session['discount'] = 20
            messages.success(request, 'FESTIVE20 applied! 20% discount added.')

        else:
            request.session['discount'] = 0
            messages.error(request, 'Invalid coupon code')

    return redirect('cart')






@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    # ✅ DEFINE cart_total HERE
    cart_total = sum(item.product.price * item.quantity for item in cart_items)

    if request.method == "POST":
        order = Order.objects.create(
            user=request.user,
            total_amount=cart_total
        )

        cart_items.delete()
        return redirect('order_success')

    return render(request, 'store/checkout.html', {
        'cart_items': cart_items,
        'cart_total': cart_total
    })



def search(request):
    query = request.GET.get('q')

    products = []
    if query:
        products = Product.objects.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__icontains=query)
        )

    return render(request, 'store/search_results.html', {
        'products': products,
        'query': query
    })



@login_required
def orders(request):
    user_orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/orders.html', {
        'orders': user_orders
    })


@login_required
def track_order(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)
    return render(request, 'store/track_order.html', {'order': order})




@login_required
def place_order(request):
    order = Order.objects.create(user=request.user)

    send_mail(
        subject="Order Confirmation",
        message=f"Your order #{order.id} has been placed successfully!",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[request.user.email],
        fail_silently=False,
    )

    return redirect('orders')


def shipping_policy(request):
    return render(request, "shipping_policy.html")



def return_refund_policy(request):
    return render(request, "return_refund_policy.html")

def privacy_policy(request):
    return render(request, "privacy_policy.html")

def terms_of_service(request):
    return render(request, "terms_of_service.html")
