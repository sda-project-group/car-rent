from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from .forms import LoginForm, RegistrationForm
from django.urls import reverse_lazy, reverse
from .forms import RegistrationForm
from django.views import View


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

