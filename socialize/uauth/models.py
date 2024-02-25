from django.db import models
from django.contrib.auth.models import User
import uuid
from datetime import datetime

class U_Profile(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    id_user = models.IntegerField(primary_key=True,default=0)
    about = models.TextField(blank=True,default='')
    profilepic = models.ImageField(upload_to='profile_images',default='blank-profile-picture-973460_960_720.webp')
    
    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=100)
    image = models.ImageField(upload_to='post_images')
    caption = models.TextField()
    posted_at = models.DateTimeField(default=datetime.now)
    likes_count = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class Likes(models.Model):
    post_id = models.CharField(max_length = 400)
    username = models.CharField(max_length = 100)

    def __str__(self):
        return self.username