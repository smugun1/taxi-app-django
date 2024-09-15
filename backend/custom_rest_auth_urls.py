from django.urls import path
from dj_rest_auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='rest_login'),  # Optional if not using custom login
    path('logout/', LogoutView.as_view(), name='rest_logout'),
    path('password/reset/', PasswordResetView.as_view(), name='rest_password_reset'),
    path('password/reset/confirm/', PasswordResetConfirmView.as_view(), name='rest_password_reset_confirm'),
    path('password/change/', PasswordChangeView.as_view(), name='rest_password_change'),
]
