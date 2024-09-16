from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static
from .views import (
    StatsView, LogoutView, CustomRegisterView, CustomTokenObtainPairView,
    RideListCreateView, RideDetailView, RideAcceptView, RideCompleteView,
    LocationListCreateAPIView, LocationDetailAPIView, TransactionListView,
    PaymentIntentView, UserListView, UserCreateView, create_checkout_session, get_user, save_location,
    DriverLicenseListView, DriverLicenseCreateView, VehicleListView, VehicleCreateView
)

urlpatterns = [
    # JWTAuthentication refresh tokens
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Auth and User Management
    path('api/auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('api/auth/register/', CustomRegisterView.as_view(), name='register'),
    path('api/auth/logout/', LogoutView.as_view(), name='logout'),

    # Dashboard statistics
    path('stats/', StatsView.as_view(), name='stats'),

    # Rides Management
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('rides/accept/<int:ride_id>/', RideAcceptView.as_view(), name='ride-accept'),
    path('rides/complete/<int:ride_id>/', RideCompleteView.as_view(), name='ride-complete'),

    # Locations
    path('api/locations/', LocationListCreateAPIView.as_view(), name='location-list-create'),
    path('api/locations/<int:pk>/', LocationDetailAPIView.as_view(), name='location-detail'),

    # Transactions and Payments
    path('transaction-list/', TransactionListView.as_view(), name='transaction-list'),
    path('payments/intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),

    # User Management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/get-user/', get_user, name='get_user'),

    # Driver Licenses and Vehicles
    path('driver-license/', DriverLicenseListView.as_view(), name='driver-license-list'),
    path('driver-license/create/', DriverLicenseCreateView.as_view(), name='driver-license-create'),
    path('vehicle/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicle/create/', VehicleCreateView.as_view(), name='vehicle-create'),

    # Location Saving
    path('location/save/', save_location, name='save-location'),

    # Registration-related URLs
    path('accounts/', include('registration.backends.default.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
