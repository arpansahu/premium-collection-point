from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


# Create your models here.
from account.choices import ROLE_CHOICES


class MyAccountManager(BaseUserManager):
    def create_user(self, email, username, password):
        if not email:
            raise ValueError("User must have a valid email ")
        if not username:
            raise ValueError("User must have a valid username")
        if not password:
            raise ValueError("Enyter a correct password")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )

        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_kyc = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.IntegerField(choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=10)
    adhaar_number = models.CharField(max_length=12)
    pan = models.CharField(max_length=10)
    wallet_balance = models.FloatField(default=0.00)
    supervisor = models.CharField(max_length=60)
    referred_by = models.EmailField(verbose_name="email", max_length=60, default='admin@arpansahu.me')
    drive = models.URLField(default="#")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'password']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_supervisor(self):
        return self.supervisor

    def get_is_kyc(self):
        return self.is_kyc
