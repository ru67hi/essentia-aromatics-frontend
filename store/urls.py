from django.urls import path
from . import views

urlpatterns = [
    # Home
    path('', views.home, name='home'),

    # Products
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product, name='product'),

    # Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),
    path('cart/increase/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    # Auth
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.orders, name='orders'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),

    # Search
    path('search/', views.search, name='search'),

    # Contact
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),





   path('', views.home, name='home'),
   path('hampers/', views.hamper_products, name='hamper_products'),

   path("shipping-policy/", views.shipping_policy, name="shipping_policy"),
   path("return-refund-policy/", views.return_refund_policy, name="return_refund_policy"),
   path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
   path("terms-of-service/", views.terms_of_service, name="terms_of_service"),


]