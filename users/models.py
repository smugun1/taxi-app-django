from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings

# Custom user manager to handle the creation of users and superusers
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        if not username:
            raise ValueError('The Username field must be set')  # Ensure the username is provided

        email = self.normalize_email(email)  # Normalize the email address
        user = self.model(email=email, username=username, **extra_fields)  # Create a new user instance
        user.set_password(password)  # Set the user's password
        user.save(using=self._db)  # Save the user to the database
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)  # Ensure 'is_staff' is set to True
        extra_fields.setdefault('is_superuser', True)  # Ensure 'is_superuser' is set to True

        # Validate the 'is_staff' field
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        # Validate the 'is_superuser' field
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, username, password, **extra_fields)  # Create a superuser using the create_user method
# Custom user model that extends Django's AbstractBaseUser and PermissionsMixin
class CustomUser(AbstractBaseUser, PermissionsMixin):
    # Define user type choices
    USER_TYPE_CHOICES = (
        (1, 'admin'),
        (2, 'driver'),
        (3, 'passenger'),
    )

    email = models.EmailField(unique=True)  # Email field that is unique for each user
    username = models.CharField(max_length=150, unique=True)  # Ensure username is included
    password = models.CharField(max_length=128)  # Include if needed, though password is typically handled by AbstractBaseUser
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, default=2)  # User type field with predefined choices
    is_staff = models.BooleanField(default=False)  # Boolean to indicate if the user is a staff member
    is_active = models.BooleanField(default=True)  # Boolean to indicate if the user is active

    objects = CustomUserManager()  # Assign the custom user manager to this model

    USERNAME_FIELD = 'email'  # Set email as the username field for authentication
    REQUIRED_FIELDS = ['username', 'user_type']  # Fields required when creating a user via createsuperuser

    class Meta:
        ordering = ['-id']  # Set default ordering by id in descending order

    def __str__(self):
        return self.email  # String representation of the user model

# Model for storing driver's license details
class DriverLicense(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='license')  # One-to-one relationship with CustomUser
    license_number = models.CharField(max_length=50)  # License number field
    issue_date = models.DateField()  # Date field for license issue date
    # Add other fields as needed for license details

# Model for storing vehicle details
class Vehicle(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='vehicles')  # Foreign key relationship with CustomUser
    make = models.CharField(max_length=100)  # Vehicle make field
    model = models.CharField(max_length=100)  # Vehicle model field
    registration_number = models.CharField(max_length=20)  # Vehicle registration number
    # Add other fields for vehicle details like insurance, etc.

# Model for storing ride details
class Ride(models.Model):
    # Status choices for ride status
    STATUS_CHOICES = [
        ('requested', 'Requested'),
        ('accepted', 'Accepted'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    passenger = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rides_as_passenger', on_delete=models.CASCADE)  # Foreign key to CustomUser for the passenger
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='rides_as_driver', on_delete=models.SET_NULL, null=True, blank=True)  # Foreign key to CustomUser for the driver, can be null
    origin = models.CharField(max_length=255)  # Origin of the ride
    destination = models.CharField(max_length=255)  # Destination of the ride
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='requested')  # Ride status field with predefined choices
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the ride was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for when the ride was last updated
    pickup_time = models.DateTimeField(null=True, blank=True)  # Time when the driver starts picking up
    dropoff_time = models.DateTimeField(null=True, blank=True)  # Time when the passenger is dropped off

    def __str__(self):
        return f"Ride from {self.origin} to {self.destination} ({self.status})"  # String representation of the ride model

# Model for storing transaction details
class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Foreign key relationship with CustomUser
    amount = models.DecimalField(max_digits=10, decimal_places=2)  # Field for transaction amount
    description = models.CharField(max_length=255)  # Field for transaction description
    timestamp = models.DateTimeField(auto_now_add=True)  # Timestamp for when the transaction occurred

    def __str__(self):
        return f'Transaction of ${self.amount} for {self.description} on {self.timestamp}'  # String representation of the transaction model
