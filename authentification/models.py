from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Permission, Group


class Level(models.Model):
    label = models.CharField(max_length=50, null=True)
    capacity = models.IntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.label
    
    def serialize(self):
        return {
            'id': self.id,
            'label': self.label,
            'capacity': self.capacity,
        }

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'email est requis.")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("Le superutilisateur doit avoir la permission 'is_staff'.")
        if extra_fields.get('is_superuser') is not True:
            raise ValueError("Le superutilisateur doit avoir la permission 'is_superuser'.")

        return self.create_user(email, password, **extra_fields)


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,null=True
    )
    first_name = models.CharField(max_length=40, null=True, blank=True)
    last_name = models.CharField(max_length=40,null=True, blank=True)
    password = models.CharField(max_length=255)
    level = models.ForeignKey(
        Level, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_teacher = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'email'

    groups = models.ManyToManyField(Group, related_name='myuser_groups', blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name='myuser_permissions', blank=True)

    def __str__(self) -> str:
        return self.email

    def serialize(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }
    
    def is_reset_token_valid(self, token):
        return self.reset_token == token

    def is_reset_token_expired(self):
        return self.reset_token_expiration is not None and self.reset_token_expiration < timezone.now()