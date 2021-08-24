from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    PasswordChangeForm, AuthenticationForm
from django.forms.widgets import NumberInput, Select, EmailInput, TextInput
from django_countries.fields import CountryField
from .models import CustomUser, Gender, image
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation, authenticate
from clothing_store import settings
from django.utils import timezone

attrs_ = {'class': 'form-control'}


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=EmailInput(attrs=attrs_))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_


default_image = {
    "Male": "account_image/default_account_image/Man default_image.jpg",
    "Female": "account_image/default_account_image/Woman_default_image.jpg",
    "Not specified": image}

gender_dict = {'N': 'Not specified', 'F': 'Female', 'M': 'Male'}


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['user_name', 'country', 'city', 'birth_date', 'gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_

    @property
    def age_valid(self):
        if (timezone.now().year - self.cleaned_data['birth_date'].year - (
                (timezone.now().month, timezone.now().day) <
                (self.cleaned_data['birth_date'].month,
                 self.cleaned_data['birth_date'].day))) > 1:
            return True

        return False

    @staticmethod
    def image(image_, gender_):
        if image_ in default_image.values():
            return default_image[gender_]
        return image_

    def save(self):
        user = super().save(commit=False)
        user.gender = gender_dict[self.cleaned_data['gender']]
        user.main_image = self.image(user.main_image, user.gender)
        user.save()
        return user


class ImageForm(forms.Form):
    main_image = forms.ImageField(required=False)

    def save(self, user):
        user.main_image = self.cleaned_data['main_image']
        user.save()


class ChangePasswordForm(PasswordChangeForm):
    def __init__ (self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_


class ChangeEmailForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_))
    new_email = forms.CharField(widget=EmailInput(attrs=attrs_))
    repeat_new_email = forms.CharField(widget=EmailInput(attrs=attrs_))

    class Meta:
        model = CustomUser
        fields = ['email']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs = attrs_

    def is_valid(self):
        if super().is_valid():
            new_email = self.cleaned_data['new_email']
            repeat_new_email = self.cleaned_data['repeat_new_email']
            user = authenticate(
                password=self.cleaned_data['password'],
                email=self.cleaned_data['email']
            )
            if user is None:
                return False

            if new_email != repeat_new_email:
                return False

            return True
        return False

    def save(self):
        user = super().save(commit=False)
        user.email = self.cleaned_data['new_email']
        user.save()
        return user
