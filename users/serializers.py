from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    profileImage_url = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['id', 'name', 'email', 'password', 'weight', 'height', 'profileImage' , 'profileImage_url']
        extra_kwargs ={
            'password' : {'write_only':True}
        }
<<<<<<< HEAD
    def get_profileImage_url(self, obj):
        request = self.context.get('request')
        if obj.profileImage and request:
            url = request.build_absolute_uri(obj.profileImage.url)
            if url.startswith('http://'):
                url = url.replace('http://', 'https://', 1)
            return url
        return None
    
=======
>>>>>>> 60cf6dff7d8a295d8f4a0496c08a754cf45b59f6
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance