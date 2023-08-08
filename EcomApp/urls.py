from django.urls import path
from EcomApp.views import ProductView, ProductDetailView, ProfileView
from . import views
from django.contrib.auth import views as auth_view
from .forms import LoginForm, MyPasswordChangeForm, MyPasswordResetForm, MySetpasswordForm


urlpatterns = [
    path('',  ProductView.as_view() , name='home_page'),
    path('product-detail/<int:pk>', ProductDetailView.as_view(), name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='showcart'),
    path('checkout/', views.checkout, name='checkout'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('paymentdone/', views.payment_done, name='payment-done'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),

    path('registration/', views.customerregistration, name='customerregistration'),
    path('login/', auth_view.LoginView.as_view(template_name='EcomApp/login.html',
                                               authentication_form=LoginForm), name='login'),
    path('logout/', auth_view.LogoutView.as_view(next_page='login'), name='logout'),
   
    path('passwordchange/', auth_view.PasswordChangeView.as_view
         (template_name='EcomApp/passwordchange.html', form_class=MyPasswordChangeForm,
          success_url='/passwordchangedone/'), name='passwordchange'),

    path('passwordchangedone/', auth_view.PasswordChangeDoneView.as_view
         (template_name='EcomApp/passwordchangedone.html'), name='passwordchangedone'),

    path('password-reset/', auth_view.PasswordResetView.as_view
         (template_name='EcomApp/password_reset.html', 
          form_class=MyPasswordResetForm), name='password_reset'),

    path('password-reset-done/', auth_view.PasswordResetDoneView.as_view
         (template_name='EcomApp/password_reset_done.html'), name='password_reset_done'),

    path('password-reset-confirm/<uidb64>/<token>/', auth_view.PasswordResetConfirmView.as_view
         (template_name='EcomApp/password_reset_confirm.html',
          form_class=MySetpasswordForm), name='password_reset_confirm'),

    path('password-reset-complete/', auth_view.PasswordResetCompleteView.as_view
         (template_name='EcomApp/password_reset_complete.html'), name='password_reset_complete'),

   
    path('admin-view/', views.admin_view, name='admin-view'),
    
]
