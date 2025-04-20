from rest_framework import serializers
from .models import UserImage ,UserClothes

class UserImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserImage
        fields = ['id', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            url = request.build_absolute_uri(obj.image.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None



class UserClothesImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = UserClothes
        fields = ['id', 'image', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and request:
            url = request.build_absolute_uri(obj.image.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None