from django.db import models
from users.models import User
import os
from uuid import uuid4

def user_image_upload_to(instance, filename):
    # Get the user's email
    user_email = instance.user.email
    # Generate a unique filename
    unique_filename = str(uuid4())
    # Split the original filename and get its extension
    _, extension = os.path.splitext(filename)
    # Construct the file path
    return f'user_images/{user_email}/{unique_filename}{extension}'

def clothes_image_upload_to(instance, filename):
    # Get the user's email
    user_email = instance.user.email
    # Generate a unique filename
    unique_filename = str(uuid4())
    # Split the original filename and get its extension
    _, extension = os.path.splitext(filename)
    # Construct the file path
    return f'user_clothes/{user_email}/{unique_filename}{extension}'

class UserImage(models.Model):
    user = models.ForeignKey(User, related_name='user_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=user_image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)

class UserClothes(models.Model):
    user = models.ForeignKey(User, related_name='clothes_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=clothes_image_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
