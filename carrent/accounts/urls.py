from django.contrib.auth import views as auth_views
from django.urls import path


from .forms import LoginForm
from .views import CustomLoginView, RegisterView, ChangePasswordView, UpdateProfileUserView


urlpatterns = [
    path('login/', CustomLoginView.as_view(redirect_authenticated_user=True, template_name='accounts/login.html',
                                           authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='accounts/logout.html'), name='logout'),
    path('registration/', RegisterView.as_view(), name='users-registration'),
    path('profile/', UpdateProfileUserView.as_view(), name='user-profile'),
    path('password-change/', ChangePasswordView.as_view(), name='password_change'),
]
