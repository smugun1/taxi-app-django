from datetime import timezone
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
import stripe
from django.conf import settings
from rest_framework import serializers
# from django.views import View
from registration.backends.default.views import RegistrationView

from .models import CustomUser, DriverLicense, Location, Ride, Vehicle, Transaction
from .serializers import (
    CustomRegisterSerializer,
    CustomUserSerializer,
    DriverLicenseSerializer,
    LocationSerializer,
    RegisterSerializer,
    RideSerializer,
    TransactionSerializer,
    VehicleSerializer
)
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.views import APIView

from users import serializers
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login as auth_login
from rest_framework_simplejwt.tokens import RefreshToken
import logging

logger = logging.getLogger(__name__)


# Set the Stripe API key from Django settings
stripe.api_key = settings.STRIPE_SECRET_KEY

# Get the custom user model
User = get_user_model()

def get_user(request):
    # Your logic to get user
    return JsonResponse({'user': 'user-data'})

# # Serializer for Register
# # Make sure your import looks like this for ModelSerializer
# class RegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)

#     class Meta:
#         model = User
#         fields = ('username', 'password')

#     def create(self, validated_data):
#         user = User.objects.create_user(
#             username=validated_data['username'],
#             password=validated_data['password']
#         )
#         return user

# Register View
class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View
class LoginView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)
        if user is not None:
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# Logout View
class LogoutView(APIView):
    def post(self, request):
        try:
            request.user.auth_token.delete()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_204_NO_CONTENT)
        except:
            return Response({'error': 'Failed to log out'}, status=status.HTTP_400_BAD_REQUEST)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    A custom view for obtaining JWT tokens, allowing you to customize the response or authentication process.
    """
    # You can override the serializer class to use a custom serializer if needed
    # serializer_class = TokenObtainPairSerializer
    pass

# Ride acceptance view
class RideAcceptView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        try:
            ride = Ride.objects.get(id=ride_id)
            if ride.status != 'requested':
                return Response({'error': 'Ride is not available for acceptance.'}, status=status.HTTP_400_BAD_REQUEST)

            ride.driver = request.user
            ride.status = 'accepted'
            ride.pickup_time = timezone.now()  # Mark the pickup time
            ride.save()
            return Response({'status': 'Ride accepted', 'ride_id': ride.id})
        except Ride.DoesNotExist:
            return Response({'error': 'Ride not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Ride completion view
class RideCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, ride_id):
        ride = Ride.objects.get(id=ride_id)
        if ride.status != 'in_progress':
            return Response({'error': 'Ride is not in progress.'}, status=status.HTTP_400_BAD_REQUEST)

        ride.status = 'completed'
        ride.dropoff_time = timezone.now()  # Mark the drop-off time
        ride.save()

        # Process payment (using Stripe or any other method)
        # payment processing logic here...

        return Response({'status': 'Ride completed', 'ride_id': ride.id})


# API view to list and create rides
class RideListCreateView(generics.ListCreateAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    # Automatically set the passenger to the current user
    def perform_create(self, serializer):
        serializer.save(passenger=self.request.user)


# API view to retrieve, update, and delete a specific ride
class RideDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Ride.objects.all()
    serializer_class = RideSerializer
    permission_classes = [IsAuthenticated]

    # Custom update method to handle ride status changes
    def update(self, request, *args, **kwargs):
        ride = self.get_object()
        if 'status' in request.data:
            ride.status = request.data['status']
            ride.save()
        serializer = self.get_serializer(ride)
        return Response(serializer.data)

class LocationListCreateAPIView(APIView):
    """
    View to list all locations or create a new location.
    """
    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LocationDetailAPIView(APIView):
    """
    View to retrieve, update, or delete a location by ID.
    """
    def get_object(self, pk):
        try:
            return Location.objects.get(pk=pk)
        except Location.DoesNotExist:
            return None

    def get(self, request, pk):
        location = self.get_object(pk)
        if location is None:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

    def put(self, request, pk):
        location = self.get_object(pk)
        if location is None:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        serializer = LocationSerializer(location, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        location = self.get_object(pk)
        if location is None:
            return Response({'error': 'Location not found'}, status=status.HTTP_404_NOT_FOUND)
        location.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# API view to list and create transactions
class TransactionListView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    # Restrict transactions to the current user
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    # Automatically set the user for the transaction to the current user
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# Dashboard statistics view
class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        total_rides = Ride.objects.count()
        completed_rides = Ride.objects.filter(status='completed').count()
        pending_rides = Ride.objects.filter(status='requested').count()
        canceled_rides = Ride.objects.filter(status='canceled').count()

        stats = {
            'totalRides': total_rides,
            'completedRides': completed_rides,
            'pendingRides': pending_rides,
            'canceledRides': canceled_rides
        }
        return Response(stats, status=status.HTTP_200_OK)

@csrf_exempt
def create_checkout_session(request):
    logger.info('Received request to create checkout session')
    YOUR_DOMAIN = "http://localhost:3000"

    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': 'Sample Product',
                        },
                        'unit_amount': 2000,  # amount in cents
                    },
                    'quantity': 1,
                },
            ],
            mode='payment',
            success_url=YOUR_DOMAIN + '/success',
            cancel_url=YOUR_DOMAIN + '/cancel',
        )
        return JsonResponse({
            'id': checkout_session.id
        })
    except Exception as e:
        return JsonResponse({'error': str(e)})

# Payment Intent View for Stripe integration
class PaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            # Create a Stripe payment intent
            intent = stripe.PaymentIntent.create(
                amount=5000,  # Amount in cents
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'clientSecret': intent['client_secret']})
        except Exception as e:
            return Response({'error': str(e)})


# Custom registration view using a custom serializer
class CustomRegisterView(RegistrationView):
    serializer_class = CustomRegisterSerializer


# API view to list all users
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


# API view to create a new user
class UserCreateView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer


# API view to list all driver licenses
class DriverLicenseListView(generics.ListAPIView):
    queryset = DriverLicense.objects.all()
    serializer_class = DriverLicenseSerializer


# API view to create a new driver license
class DriverLicenseCreateView(generics.CreateAPIView):
    queryset = DriverLicense.objects.all()
    serializer_class = DriverLicenseSerializer


# API view to list all vehicles
class VehicleListView(generics.ListAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


# API view to create a new vehicle
class VehicleCreateView(generics.CreateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer


# Custom serializer for obtaining JWT tokens with additional validation
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Add custom claims here if needed
        return token

    # Custom validation for email and password authentication
    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password')
        }

        user = CustomUser.objects.filter(email=credentials['email']).first()

        if user is None:
            raise serializers.ValidationError('No user with this email found.')

        if not user.check_password(credentials['password']):
            raise serializers.ValidationError('Incorrect password.')

        return super().validate(attrs)


# Custom view to obtain JWT tokens
class CustomTokenObtainPairView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh)
            })
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


# Function-based view to save a location
@api_view(['POST'])
def save_location(request):
    try:
        location = request.data.get('location')
        if not location:
            return Response({'error': 'No location provided'}, status=status.HTTP_400_BAD_REQUEST)
        # Process location (e.g., save to database)
        return Response({'message': 'Location saved successfully'}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class PaymentIntentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        try:
            intent = stripe.PaymentIntent.create(
                amount=5000,  # Amount in cents
                currency='usd',
                payment_method_types=['card'],
            )
            return Response({'clientSecret': intent['client_secret']})
        except stripe.error.CardError as e:
            return Response({'error': 'Card error: {}'.format(e.user_message)}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.RateLimitError:
            return Response({'error': 'Rate limit error.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)
        except stripe.error.InvalidRequestError:
            return Response({'error': 'Invalid request.'}, status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.AuthenticationError:
            return Response({'error': 'Authentication error.'}, status=status.HTTP_401_UNAUTHORIZED)
        except stripe.error.APIConnectionError:
            return Response({'error': 'Network communication error.'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        except stripe.error.StripeError as e:
            return Response({'error': 'Stripe error: {}'.format(e.user_message)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
