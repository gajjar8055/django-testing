from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractUser):
    pass
