from rest_framework import serializers
from .models import UserImage ,UserClothes

class UserImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImage
        fields = ['id', 'image']



class UserClothesImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserClothes
        fields = ['id', 'image']