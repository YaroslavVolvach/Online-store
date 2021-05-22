from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, \
    PasswordChangeForm
from django.forms.widgets import NumberInput, Select, EmailInput, TextInput
from django_countries.fields import CountryField
from .models import CustomUser, Gender, image
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth import password_validation
from clothing_store import settings
from django.utils import timezone

attrs_ = {'class': 'form-control'}


class LoginForm(forms.Form):
    email = forms.CharField(widget=EmailInput(attrs=attrs_))
    password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_))


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('user_name', 'email')

    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_


default_image = {
    "Male": "account_image/default_account_image/Man default image.jpg",
    "Female": "account_image/default_account_image/Woman_default_image.jpg",
    "Not specified": image}

gender_dict = {'N': 'Not specified', 'F': 'Female', 'M': 'Male'}


class ChangeProfileForm(forms.Form):
    user_name = forms.CharField(widget=TextInput())
    country = CountryField().formfield(widget=Select())
    city = forms.CharField(widget=Select(), required=False)
    birth_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField(choices=Gender, widget=Select())
    email = forms.EmailField(widget=EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    field_exception = ('Country', 'City', 'Birth date', 'Gender')

    message = 'Your age cannot be younger then 1 year'

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

    def save(self, user):
        user.user_name = self.cleaned_data['user_name']
        user.country = self.cleaned_data['country']
        user.birth_date = self.cleaned_data['birth_date']
        user.gender = gender_dict[self.cleaned_data['gender']]
        user.main_image = self.image(user.main_image, user.gender)
        user.save()


class ImageForm(forms.Form):
    main_image = forms.ImageField(required=False)

    def save(self, user):
        user.main_image = self.cleaned_data['main_image']
        user.save()


class ChangePasswordForm(PasswordChangeForm):
    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)
        for key in self.fields.keys():
            self.fields[key].widget.attrs = attrs_


class ChangeEmailForm(LoginForm):
    new_email = forms.CharField(widget=EmailInput(attrs=attrs_))
    repeat_new_email = forms.CharField(widget=EmailInput(attrs=attrs_))

    def email_valid(self, user):
        if self.cleaned_data['new_email'] == self.cleaned_data[
                                                        'repeat_new_email']:
            self.save(user)
            return False
        return True

    def save(self, user):
        user.email = CustomUser.objects.normalize_email(self.cleaned_data[
                                                      'new_email'])
        user.save()