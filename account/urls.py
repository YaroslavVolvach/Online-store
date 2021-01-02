from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

app_name = 'account'

urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login_, name='login'),
    path('logout/', views.logout_, name='logout')]

# path('logout/', views.logout, name='logout')
