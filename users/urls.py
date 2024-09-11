from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    CustomRegisterView,
    RideAcceptView,
    RideCompleteView,
    RideListCreateView,
    RideDetailView,
    TransactionListView,
    DashboardStatsView,
    PaymentIntentView,
    UserListView,
    UserCreateView,
    DriverLicenseListView,
    DriverLicenseCreateView,
    VehicleListView,
    VehicleCreateView,
    CustomTokenObtainPairView,
    save_location,
)
from . import views

urlpatterns = [
    path('auth/register/', CustomRegisterView.as_view(), name='register'),
     path('accounts/', include('registration.backends.default.urls')),
    path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('rides/', RideListCreateView.as_view(), name='ride-list-create'),
    path('rides/<int:pk>/', RideDetailView.as_view(), name='ride-detail'),
    path('rides/accept/<int:ride_id>/', RideAcceptView.as_view(), name='ride-accept'),
    path('rides/complete/<int:ride_id>/', RideCompleteView.as_view(), name='ride-complete'),
    path('transactions/', TransactionListView.as_view(), name='transaction-list'),
    path('dashboard-stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('payments/intent/', PaymentIntentView.as_view(), name='payment-intent'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/create/', UserCreateView.as_view(), name='user-create'),
     path('api/get-user/', views.get_user, name='get_user'),
    path('driver-licenses/', DriverLicenseListView.as_view(), name='driver-license'),
    path('driver-licenses/create/', DriverLicenseCreateView.as_view(), name='driver-license-create'),
    path('vehicles/', VehicleListView.as_view(), name='vehicle-list'),
    path('vehicles/create/', VehicleCreateView.as_view(), name='vehicle-create'),
    path('location/save/', save_location, name='save-location'),
]
