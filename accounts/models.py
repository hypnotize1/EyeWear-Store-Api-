from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import  AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# Create your models here.

class CustomUserManager(BaseUserManager):
    """
        Custom manager for CustomUser model.

        Provides methods to create regular users and superusers using email as
        the unique identifier instead of username.

        Methods:
            create_user(email, password, **extra_fields):
                Creates and saves a regular user.

            create_superuser(email, password, **extra_fields):
                Creates and saves a superuser with all required flags.
        """

    def create_user(self, email, password, **extra_fields):
        """
           Create and save a new user with the given email and password.

        """
        if not email:
            raise ValueError('Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a superuser with the given email and password.

        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    """
    Custom user model that replaces Django's default User model.

    This model uses email instead of username as the primary identifier
    for authentication.

    Fields:
        name (str): Full name of the user.
        email (str): Unique email address used for login.
        phone (str): Unique Iranian phone number in the format 09xxxxxxxxx.
        is_staff (bool): Determines whether the user can access the admin site.
        is_active (bool): Indicates whether this user account is active.
        date_joined (datetime): Date and time when the user account was created.
        last_login (datetime): Automatically updated when the user logs in.

    Authentication:
        USERNAME_FIELD: 'email' is used as the unique identifier for login.
        REQUIRED_FIELDS: ['name', 'phone'] are required when using createsuperuser.

    Manager:
        objects: CustomUserManager is used to handle user creation and management.
    """
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=11, unique=True, validators=[
        RegexValidator(regex=r'^09\d{9}$', message='Phone number must be in format 09xxxxxxxxx')]
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone']

    objects = CustomUserManager()

