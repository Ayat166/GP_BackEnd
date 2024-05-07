from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from generated.serializers import UserGeneratedImageSerializer
from users.models import User
from cloths.serializers import UserImageSerializer , UserClothesImageSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt

# Create your views here.


class UserGeneratedView(APIView):
    def post(self, request):
        try:
            user_image_data = {"image": request.data["user_image"]}
            user_cloth_data = {"image": request.data["user_cloth"]}
        except KeyError:
            return Response({"error": "Both user_image and user_cloth data are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializerImage = UserImageSerializer(data=user_image_data)
        serializerClothes = UserClothesImageSerializer(data=user_cloth_data)
        if serializerImage.is_valid() and serializerClothes.is_valid():
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            user = User.objects.filter(id=payload['id']).first()
            user_image_instance = serializerImage.save(user=user)
            user_clothes_instance = serializerClothes.save(user=user)
            generated_image = user_image_instance.image
            serializer_generated_image = UserGeneratedImageSerializer(data={
                'user': user.id,
                'user_image': user_image_instance.id,
                'user_clothes': user_clothes_instance.id,
                'generated_image': generated_image
            })
            if serializer_generated_image.is_valid():
                user_generated_image_instance = serializer_generated_image.save()
                return Response(serializer_generated_image.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_generated_image.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response([serializerImage.errors, serializerClothes.errors], status=status.HTTP_400_BAD_REQUEST)
    
    
