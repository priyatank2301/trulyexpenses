from .views import RegistrationView,UsernameValidationView,EmailValidationView,VerificationView,LoginView,LogoutView,RequestPasswordResetEmail,CompletePasswordReset
from django.urls import path
from django.views.decorators.csrf import csrf_exempt,csrf_protect

urlpatterns = [
    path('register/', RegistrationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    
    path('validate-username/', csrf_exempt(UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/',csrf_exempt (EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>',csrf_exempt (VerificationView.as_view()), name='activate'),
    path('password-reset/',csrf_exempt (RequestPasswordResetEmail.as_view()), name='request-password'),
    path('set_new_password/<uidb64>/<token>',csrf_exempt (CompletePasswordReset.as_view()), name='reset-user-password'),
    
    ]