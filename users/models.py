from django.contrib.auth.models import AbstractBaseUser,    BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):

  def _create_user(self, email, password, is_staff, is_superuser, name, surname):
    if not email:
        raise ValueError('Users must have an email address')
    now = timezone.now()
    email = self.normalize_email(email)
    user = self.model(
        email=email,
        is_staff=is_staff, 
        is_active=True,
        is_superuser=is_superuser, 
        last_login=now,
        date_joined=now, 
        name=name,
        surname=surname,
    )
    user.set_password(password)
    user.save(using=self._db)
    return user

  def create_user(self, email, password, name, surname):
    return self._create_user(email, password, False, False, name, surname)

  def create_superuser(self, email, password, name, surname):
    user=self._create_user(email, password, True, True, name, surname)
    user.save(using=self._db)
    return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=254, unique=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=25, null=True, blank=True)
    surname = models.CharField(max_length=25, null=True, blank=True)    

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['name','surname']

    objects = UserManager()

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)