from rest_framework import serializers
from .models import UserGeneratedImage

class UserGeneratedImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserGeneratedImage
        fields = ['id','user', 'user_image', 'user_clothes', 'generated_image', 'is_fav']
