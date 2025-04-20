from rest_framework import serializers
from .models import UserGeneratedImage

class UserGeneratedImageSerializer(serializers.ModelSerializer):
<<<<<<< HEAD
    generated_image_url = serializers.SerializerMethodField()
    class Meta:
        model = UserGeneratedImage
        fields = ['id','user', 'user_image', 'user_clothes', 'generated_image', 'is_fav' , 'generated_image_url']
        
    def get_generated_image_url(self, obj):
        request = self.context.get('request')
        if obj.generated_image and request:
            url = request.build_absolute_uri(obj.generated_image.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None


class UserGeneratedImageSerializerRetrive(serializers.ModelSerializer):
    generated_image_url = serializers.SerializerMethodField()
    class Meta:
        model = UserGeneratedImage
        fields = ['id','generated_image', 'is_fav' , 'generated_image_url']
        
    def get_generated_image_url(self, obj):
        request = self.context.get('request')
        if obj.generated_image and request:
            url = request.build_absolute_uri(obj.generated_image.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None
=======
    class Meta:
        model = UserGeneratedImage
        fields = ['id','user', 'user_image', 'user_clothes', 'generated_image', 'is_fav']
>>>>>>> 60cf6dff7d8a295d8f4a0496c08a754cf45b59f6
