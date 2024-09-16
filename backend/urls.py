from django.contrib import admin
from django.urls import path, include
from users.views import CustomRegisterView, TransactionListView, PaymentIntentView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),  # Users app URL configuration
    path('api/', include('geocoding.urls')),  # Geocoding URL configuration
    path('api/auth/', include('backend.custom_rest_auth_urls')),  # Custom authentication URL config

    # Custom token obtain endpoints
    path('api/token/', CustomTokenObtainPairView.as_view(), name='custom_token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Auth-related endpoints
    path('api/auth/registration/', include('dj_rest_auth.registration.urls')),
    path('api/auth/register/', CustomRegisterView.as_view(), name='custom_register'),

    # Transactions and payment intent
    path('api/transactions/', TransactionListView.as_view(), name='transaction_list'),
    path('api/payment-intent/', PaymentIntentView.as_view(), name='payment_intent'),
]
