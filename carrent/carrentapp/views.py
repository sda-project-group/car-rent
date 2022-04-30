from django.shortcuts import render
from django.contrib.auth.views import LoginView
from .forms import LoginForm
from django.urls import reverse_lazy, reverse


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
