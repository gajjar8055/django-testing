from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth.validators import ASCIIUsernameValidator


class User(AbstractUser):
    pass


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class CPU(models.Model):
    grouped = models.BooleanField(default=True)
    slug = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    ref_id = models.CharField(max_length=200)
    link_name = models.CharField(max_length=600, default="", null=True)
