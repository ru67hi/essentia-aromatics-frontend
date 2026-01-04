from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Products
    path('products/', views.products, name='products'),
    path('product/<int:id>/', views.product, name='product'),

    # Cart
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),

    # Auth
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),

    # Contact
   
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),


    path('combos/', views.combos, name='combos'),
    path('combo/', views.combo_products, name='combo_products'),
    path('product/<int:id>/', views.product, name='product'),

    path('hampers/', views.hamper_products, name='hamper_products'),
    path('product/<int:id>/', views.product, name='product'),
   
  
    path('cart/increase/<int:item_id>/', views.increase_qty, name='increase_qty'),
    path('cart/decrease/<int:item_id>/', views.decrease_qty, name='decrease_qty'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),

    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('checkout/', views.checkout, name='checkout'),
    path('search/', views.search, name='search'),
    path('orders/', views.orders, name='orders'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path("shipping-policy/", views.shipping_policy, name="shipping_policy"),
    path("return-refund-policy/", views.return_refund_policy, name="return_refund_policy"),
    path('', views.home, name='home'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    path("", views.home, name="home"),
    path("terms-of-service/", views.terms_of_service, name="terms_of_service"),
    path('signup/', views.signup, name='signup'),
    path('hampers/', views.hamper_products, name='hamper_products'),


]



