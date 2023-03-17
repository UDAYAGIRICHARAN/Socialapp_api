from django.db import models
from django.contrib.auth.models import User
#django.db.models.JSONField
from django.db.models import JSONField

# Create your models here.
class User_auth(models.Model):
    email = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=50)
class User_followers(models.Model):
    #foreign key of user_auth
    user_email= models.CharField(max_length=100)
    follower_email= models.CharField(max_length=100)
class User_posts(models.Model):
    #foreign key of user_auth
    user_email= models.CharField(max_length=100)
    post= JSONField()
  