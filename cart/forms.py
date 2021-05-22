from django import forms


class CartAddProductForm(forms.Form):
    quantity = forms.TypedChoiceField(label='', coerce=int,
                        widget=forms.Select(attrs={'class': 'form-control'}))

    update = forms.BooleanField(required=False, initial=False,
                                widget=forms.HiddenInput)

    def __init__(self, choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['quantity'].choices = ((i, str(i)) for i in range(1,
                                                                      choices))



    #def quantity_form(self, quantity):
     #   self.fields['quantity'].choices = ((i, str(i)) for i in
      #                                     range(1, quantity))
