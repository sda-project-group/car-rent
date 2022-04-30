from django.urls import path
from django.contrib.auth import views as auth_views
from .views import CustomLoginView
from .forms import LoginForm
from . import views


urlpatterns = [
    path('',  views.base_test_view),
    path('base-test/', views.base_test_view, name='zalogowany'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='carrentapp/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='carrentapp/logout.html'), name='logout'),
]
