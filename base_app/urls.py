
from django.urls import  path
from django.contrib.auth import views as auth_views
from .views import CustomPasswordResetView

from . import views
urlpatterns = [
    path('',views.Homeview,name='home'),
    path('about/',views.Aboutview,name='about'),
    path('menu/',views.Menuview,name='menu'),
    path('book-table/',views.BookTableview,name='book-table'),
    path('feedback/',views.feedbackview,name='feedback'),
    path('add-to-cart/',views.add_to_cart,name='add-to-cart'),
    path('cart/',views.cart_page,name="cart-page"),
    path('cart/items/', views.get_cart_items, name='cart_items'),
    path('cart/remove/',views.remove_from_cart,name="remove_from_cart"),

    # order urls 
    path("checkout/", views.checkout, name="checkout"),
    path("place-order/", views.place_order, name="place_order"),
    
    # authentication pages
    path('login/',views.login_view,name='login'),
    path('signup/',views.signup_view,name='signup'),
    path('logout/',views.logout_view,name='logout'),

    #password reset or forget-password
    path('password-reset/',CustomPasswordResetView.as_view(), name='password_reset'),

    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(
             template_name='auth/password_reset_done.html'),name='password_reset_done'),


    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(
             template_name='auth/password_reset_confirm.html'),name='password_reset_confirm'),

    path('reset/done/',auth_views.PasswordResetCompleteView.as_view(
        template_name='auth/password_reset_complete.html'),name='password_reset_complete'),
]



