from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from django.urls import path
from django.views.generic import ListView, DetailView, TemplateView
from carrentapp.views import ChangePasswordView
from . import views
from .forms import LoginForm
from .views import CustomLoginView, RegisterView, profile_view
from .models import Car

urlpatterns = [
    path('base-test/', views.base_test_view, name='zalogowany'),
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='carrentapp/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='carrentapp/logout.html'), name='logout'),
    path('registration/', RegisterView.as_view(), name='users-registration'),
    path('carlist/', ListView.as_view(model=Car), name='car_list'),
    path('cardetail/<int:pk>/', DetailView.as_view(model=Car), name="car_detail"),
    path('profile/', profile_view, name='user-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
    path('', TemplateView.as_view(template_name='carrentapp/home_page.html'), name='main'),
    path('contact', TemplateView.as_view(template_name='carrentapp/contact.html'), name='contact'),
    path('aboutus', TemplateView.as_view(template_name='carrentapp/about.html'), name='about'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
