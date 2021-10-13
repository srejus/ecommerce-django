from django.urls import path
from . import views

urlpatterns=[
    path('',views.index,name='index'),
    path('products/<int:id>',views.product,name='product'),
    path('Login',views.Login,name='Login'),
    path('signup',views.signup,name='signup'),
    path('add',views.addToCart,name='add'),
    path('remove',views.remove,name='remove'),
    path('cart',views.cart,name='cart'),
    path('address',views.address,name='address'),
    path('order',views.order,name='order'),
    path('products',views.products,name='products'),
    path('contact',views.contact,name='contact'),
    path('search/<str:term>',views.search,name='search'),
    path('pincode',views.pincode,name='pincode'),
]