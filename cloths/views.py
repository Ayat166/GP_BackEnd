from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import User
from .models import UserClothes , UserImage
from .serializers import UserImageSerializer , UserClothesImageSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt

class UserImageView(APIView):
    def post(self, request ,token):
        serializer = UserImageSerializer(data=request.data)
        if serializer.is_valid():
            #token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            user = User.objects.filter(id=payload['id']).first()
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, image_id,token):
        #token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        
        # Check if the user has the specific image by ID
        user_image = UserImage.objects.filter(id=image_id).first()
        if user_image:
            if user == user_image.user:
                user_image.delete()  # Delete the specific cloth image
                return Response({'message': 'User image deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
class UserClothImageView(APIView):
    def post(self, request, token):
        serializer = UserClothesImageSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            if not token:
                raise AuthenticationFailed('Unauthenticated!')
            try:
                payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            
            user = User.objects.filter(id=payload['id']).first()
            if not user:
                raise AuthenticationFailed('User not found')

            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, token):
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        
        user = User.objects.filter(id=payload['id']).first()
        user_images = UserClothes.objects.filter(user_id=payload['id'])
        serializer = UserClothesImageSerializer(user_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, cloth_image_id,token):
        #token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        
        # Check if the user has the specific cloth image by ID
        cloth_image = UserClothes.objects.filter(id=cloth_image_id).first()
        if cloth_image:
            if user == cloth_image.user:
                cloth_image.delete()  # Delete the specific cloth image
                return Response({'message': 'User cloth image deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not have the specified cloth image'}, status=status.HTTP_404_NOT_FOUND)
    
    