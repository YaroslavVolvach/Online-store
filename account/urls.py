from django.urls import path

from django.contrib.auth import views as auth_views
from . import views
from .forms import LoginForm

app_name = 'account'

urlpatterns = [
    path('registration/', views.Registration.as_view(), name='registration'),
    path('login/', auth_views.LoginView.as_view(
        authentication_form=LoginForm,
        template_name='account/user_login.html',
        redirect_authenticated_user='catalog:product_list'
    ), name='login'),
    path('logout/',  auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change/<int:id>/', views.UpdateProfile.as_view(), name='change_profile'),
    path('profile/change_image/', views.change_image, name='change_image'),
    path('profile/remove_image/<int:id>/', views.remove_image, name='remove_image'),
    path('profile/change_password/', views.PasswordChange.as_view(), name='change_password'),
    path('profile/change_email/<int:id>', views.EmailChange.as_view(), name='change_email')]


