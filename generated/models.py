from django.db import models
from cloths.models import UserImage ,UserClothes
from users.models import User
import os
from uuid import uuid4


def user_generated_upload_to(instance, filename):
    # Get the user's email
    user_email = instance.user.email
    # Generate a unique filename
    unique_filename = str(uuid4())
    # Split the original filename and get its extension
    _, extension = os.path.splitext(filename)
    # Construct the file path
    return f'user_generated_images/{user_email}/{unique_filename}{extension}'

class UserGeneratedImage(models.Model):
    user = models.ForeignKey(User, related_name='user_generated_images', on_delete=models.CASCADE)
    user_image = models.ForeignKey(UserImage, related_name='user_image', on_delete=models.CASCADE)
    user_clothes = models.ForeignKey(UserClothes, related_name='user_cloth', on_delete=models.CASCADE)
    generated_image = models.ImageField(upload_to=user_generated_upload_to)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    is_fav = models.BooleanField(default=False)