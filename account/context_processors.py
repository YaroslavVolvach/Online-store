from django.contrib.auth import login, authenticate
from .forms import LoginForm
from .models import CustomUser


def account(request):

    return {'account': 5}
