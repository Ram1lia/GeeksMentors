from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db.utils import IntegrityError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions
from django.contrib.postgres.fields import ArrayField


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, email, password, course, month):
        if name is None:
            raise TypeError('Users should have username')
        if email is None:
            raise TypeError('Users should have email')
        user = self.model(name=name,
                          email=self.normalize_email(email), course=course, month=month)
        user.set_password(password)
        datas = (name, email)
        for data in datas:
            try:
                user.save()
            except IntegrityError:
                raise exceptions.ValidationError(f'This {data} is not available, please write another one')
        return user

    def create_superuser(self, name, email, password, course, month):
        if password is None:
            raise TypeError('Password should not be none')
        user = self.create_user(name, email, password, course, month)
        user.is_superuser = True
        user.is_staff = True
        user.set_password(password)
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):
    COURSE_CHOICES = (
        ('Backend', 'Backend'),
        ('Frontend', 'Frontend'),
        ('UX/UI', 'UX/UI'),
        ('Android', 'Android'),
        ('IOS', 'IOS')
    )

    MONTH_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
        ('7', '7'),
        ('Выпускник', 'Выпускник')
    )

    email = models.EmailField(max_length=255, unique=True, db_index=True)
    name = models.CharField(max_length=255, unique=True, db_index=True)
    image = models.ImageField(blank=True, default="mentors / default.jpg")
    course = models.CharField(choices=COURSE_CHOICES, max_length=255)
    month = models.CharField(choices=MONTH_CHOICES, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False, help_text='Email activated')
    is_staff = models.BooleanField(default=False, help_text='Работник')
    is_superuser = models.BooleanField(default=False, help_text='админ')
    is_mentor = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'course', 'month']
    objects = UserManager()

    def __str__(self):
        return self.email

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access': str(refresh.access_token),
            'refresh': str(refresh)
        }