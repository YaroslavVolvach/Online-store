from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from . import forms
from django.views import generic
from .models import CustomUser
from django.contrib.auth import password_validation, views
from django.contrib.admin.views.decorators import staff_member_required


class RegistrationView(generic.CreateView):
    form_class = forms.CustomUserCreationForm
    model = CustomUser
    success_url = '/'
    template_name = 'account/registration.html'

    def form_invalid(self, form):
        message = password_validation.password_validators_help_text_html()
        return self.render_to_response(self.get_context_data(form=form, message=message))


def profile(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    data = {'user name': user.user_name, 'email': user.email,
            'gender': user.gender, 'country': user.country.name,
            'city': user.city, 'birth date': user.birth_date}
    context = {'data': data, 'form': forms.ImageForm(), 'person': user}
    return render(request, 'account/profile.html', context)


def change_image(request):
    form = forms.ImageForm(request.POST, request.FILES)
    if form.is_valid() and form.cleaned_data['main_image'] is not None:
        form.save(request.user)
    return redirect('account:profile', request.user.id)


def remove_image(request, id):
    user = get_object_or_404(CustomUser, id=id)
    user.main_image = forms.default_image[user.gender]
    user.save()
    return redirect('account:profile', id)


class UpdateProfile(generic.UpdateView):
    form_class = forms.ChangeProfileForm
    model = CustomUser
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('account:profile')
    template_name = 'account/change_profile.html'
    message = 'This is form is not valid'

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form, message=self.message))


class PasswordChange(views.PasswordChangeView):
    form_class = forms.ChangePasswordForm
    success_url = reverse_lazy('account:profile')
    template_name = 'account/change_password.html'

    def form_invalid(self, form):
        message = password_validation.password_validators_help_text_html()
        return self.render_to_response(self.get_context_data(form=form, message=message))


class EmailChange(UpdateProfile):
    form_class = forms.ChangeEmailForm
    template_name = 'account/change_email.html'
    message = 'Password and/or email is not valid'


class UserList(generic.ListView):
    model = CustomUser
    page_kwarg = 12
    context_object_name = 'persons'
    template_name = 'account/users.html'

    def get_queryset(self):
        category = self.kwargs.get('category')
        if category == 'Staff':
            users_queryset = CustomUser.objects.filter(is_staff=True)
        elif category == 'Blocked users':
            users_queryset = CustomUser.objects.filter(is_active=False)
        elif category == 'Customers':
            users_queryset = CustomUser.objects.filter(is_active=True,
                                                       is_staff=False)
        else:
            users_queryset = CustomUser.objects.all()
        return users_queryset

    def get_context_data(self, **kwargs):
        category = self.kwargs.get('category')
        context = super().get_context_data(**kwargs)
        context['categories'] = (
                            'All users', 'Staff', 'Customers', 'Blocked users')
        if category is not None:
            context['current_category'] = category

        return context


@staff_member_required
def blacklist(request, user_id, category):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_staff or request.user.is_superuser:
        user.is_active = True if user.is_active is False else False
        user.save()
    return redirect('account:users', category)


@staff_member_required
def permissions(request, user_id, category):
    user = get_object_or_404(CustomUser, id=user_id)
    if not user.is_staff or request.user.is_superuser:
        user.is_staff = True if user.is_staff is False else False
        user.save()
    return redirect('account:users', category)

