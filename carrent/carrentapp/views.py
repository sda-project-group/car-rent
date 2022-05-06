from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import CreateView, DeleteView

from .forms import LoginForm, RegistrationForm, UpdateUserForm
from .models import BasePrice, Car, Order


def base_test_view(request):
    return render(request, 'carrentapp/base.html')


class CustomLoginView(LoginView):
    form_class = LoginForm

    def get_success_url(self):
        #tu musimy wpisać, gdzie chcemy być przekierowani po zalogowaniu - tymczasowo strona główna
        return reverse('zalogowany')

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True
        return super(CustomLoginView, self).form_valid(form)


class RegisterView(View):
    form_class = RegistrationForm
    initial = {'key': 'value'}
    template_name = 'carrentapp/registration.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            return redirect(to='zalogowany')

        return render(request, self.template_name, {'form': form})


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Twój profil został pomyślnie zaktualizowany')
            return redirect(to='user-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)

    return render(request, 'carrentapp/profile.html', {'user_form': user_form})


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'carrentapp/password_change.html'
    success_message = "Hasło zostało zmienione"
    #adres przekierowania - do zmiany
    success_url = reverse_lazy('zalogowany')


class CreateOrderView(CreateView):
    model = Order
    fields = ['start_date', 'return_date']

    def form_valid(self, form):
        objct = form.save(commit=False)
        objct.client = self.request.user
        objct.car = Car.objects.get(id=self.kwargs['pk'])
        objct.base_price = BasePrice.objects.get(id=1)
        objct.save()
        return redirect('order_confirm', pk=objct.id)



class OrderConfirmView(DeleteView):
    model = Order

    def get_success_url(self):
        return reverse('car_detail', args=[self.object.car.id])