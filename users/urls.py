from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    LogoutView, CustomRegisterView, CustomTokenObtainPairView,
    RideListCreateView, RideDetailView, RideAcceptView, RideCompleteView,
    LocationListCreateAPIView, LocationDetailAPIView, TransactionListView,
    PaymentIntentView, UserListView, UserCreateView, create_checkout_session, save_location,
    DriverLicenseListView, DriverLicenseCreateView, VehicleListView, VehicleCreateView
)
from . import views


urlpatterns = [
    # Auth and User Management
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='login'),
    # path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # Keep only one login path
    path('auth/register/', CustomRegisterView.as_view(), name='register'),  # Keep only one register path
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Rides Management
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('rides/accept/<int:ride_id>/', RideAcceptView.as_view(), name='ride-accept'),
    path('rides/complete/<int:ride_id>/', RideCompleteView.as_view(), name='ride-complete'),

    # Locations
    path('api/locations/', LocationListCreateAPIView.as_view(), name='location-list-create'),
    path('api/locations/<int:pk>/', LocationDetailAPIView.as_view(), name='location-detail'),

    # Transactions and Payments
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('payments/intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('create-checkout-session/', create_checkout_session, name='create-checkout-session'),

    # User Management
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
    path('api/get-user/', views.get_user, name='get_user'),

    # Driver Licenses and Vehicles
    path('driver-licenses/', DriverLicenseListView.as_view(), name='driver-license'),
    path('driver-licenses/create/', DriverLicenseCreateView.as_view(), name='driver-license-create'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle-create'),

    # Location Saving
    path('location/save/', save_location, name='save-location'),

    # Include registration URLs
    path('accounts/', include('registration.backends.default.urls')),
]
