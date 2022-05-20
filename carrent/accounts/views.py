from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from .validators import validation_age
from .forms import LoginForm, RegistrationForm, UpdateUserForm


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        return reverse('main')


class RegisterView(View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'accounts/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return redirect(to='main')

        return render(request, self.template_name, {'form': form})


class UpdateProfileUserView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        user_form = UpdateUserForm(instance=request.user)
        return render(request, 'accounts/profile.html', {'user_form': user_form})

    def post(self, request, *args, **kwargs):
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Twój profil został pomyślnie zaktualizowany')
            return redirect(to='user-profile')

        return render(request, 'accounts/profile.html', {'user_form': user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'accounts/password_change.html'
    success_message = "Hasło zostało zmienione"
    success_url = reverse_lazy('main')

