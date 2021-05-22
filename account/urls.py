from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('profile/change/', views.change_profile, name='change_profile'),
    path('profile/change_image/', views.change_image, name='change_image'),
    path('profile/remove_image/<int:id>/', views.remove_image, name='remove_image'),
    path('profile/change_password/', views.change_password, name='change_password'),
    path('profile/change_email/', views.change_email, name='change_email')]


