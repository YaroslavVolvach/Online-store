from .models import Order
from django import forms


class OrderForm(forms.Form):
    name = forms.CharField(label='Имя')
    family_name = forms.CharField(label='Фамилия', )
    city = forms.CharField(label='Город')
    number_phone = forms.IntegerField(label='Номер телефона')
    postcode = forms.IntegerField(label='Почтовый индекс')

    name.widget.attrs.update({'class': 'form-control'})
    family_name.widget.attrs.update({'class': 'form-control'})
    city.widget.attrs.update({'class': 'form-control'})
    number_phone.widget.attrs.update({'class': 'form-control'})
    postcode.widget.attrs.update({'class': 'form-control'})
