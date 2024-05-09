from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cloths.models import UserClothes
from generated.models import UserGeneratedImage
from generated.serializers import UserGeneratedImageSerializer
from users.models import User
from cloths.serializers import UserImageSerializer , UserClothesImageSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt
from .cloth_mask import segment_cloth
import cv2
import os
# Create your views here.
from django.core.files.base import ContentFile


class UserGeneratedView(APIView):
    # if the user upload 2 images to generate the image
    def post(self, request):
        try:
            user_image_data = {"image": request.data["user_image"]}
            user_cloth_data = {"image": request.data["user_cloth"]}
        except KeyError:
            return Response({"message": "Both user_image and user_cloth data are required."}, status=status.HTTP_400_BAD_REQUEST)
        
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
            
            # generate cloth image mask
            input_image_path = user_clothes_instance.image
            input_image = cv2.imread(str(input_image_path))
            result = segment_cloth(input_image)
            cloth_mask_image = result["cloth_mask_image"]
            output_folder = "clothMask"
            os.makedirs(output_folder, exist_ok=True)
            cloth_image_path = os.path.join(output_folder, "cloth_mask.jpg")
            cv2.imwrite(cloth_image_path, cloth_mask_image)
            #error here
            generated_image = cv2.imread(cloth_image_path)
            # Convert the numpy array to a byte string
            generated_image_bytes = cv2.imencode('.jpg', generated_image)[1].tobytes()

            # Create a ContentFile from the byte string and specify a filename
            generated_image_file = ContentFile(generated_image_bytes, name='generated_image.jpg')

            serializer_generated_image = UserGeneratedImageSerializer(data={
                'user': user.id,
                'user_image': user_image_instance.id,
                'user_clothes': user_clothes_instance.id,
                'generated_image': generated_image_file
            })
            if serializer_generated_image.is_valid():
                user_generated_image_instance = serializer_generated_image.save()
                return Response(serializer_generated_image.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer_generated_image.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response([serializerImage.errors, serializerClothes.errors], status=status.HTTP_400_BAD_REQUEST)

        
    def put(self, request, FavId):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        # Check if the user has the specific image by ID
        user_image = UserGeneratedImage.objects.filter(id=FavId).first()
        if user_image:
            if user == user_image.user:
                user_image.is_fav=True
                user_image.save()
                return Response({'message': 'User image added to Fav Successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
        
    def delete(self, request, imageId):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        user = User.objects.filter(id=payload['id']).first()
        # Check if the user has the specific image by ID
        user_image = UserGeneratedImage.objects.filter(id=imageId).first()
        if user_image:
            if user == user_image.user:
                user_image.delete()
                return Response({'message': 'User image deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
        
    
    
class UserGeneratedWithClothView(APIView):
    # if the user upload 1 image for him and choose existing cloth image to generate the image
    def post(self, request, clothimageid):
        try:
            user_image_data = {"image": request.data["user_image"]}
        except KeyError:
            return Response({"message": "user_image are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializerImage = UserImageSerializer(data=user_image_data)
        if serializerImage.is_valid():
            token = request.COOKIES.get('jwt')
            if not token:
                raise AuthenticationFailed('Unauthenticated!')
            try:
                payload = jwt.decode(token,'secret',algorithms=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated!')
            user = User.objects.filter(id=payload['id']).first()
            user_image_instance = serializerImage.save(user=user)
            user_clothes_instance = UserClothes.objects.filter(id=clothimageid).first()
            if user_clothes_instance:
                if user_clothes_instance.user == user :
                    # generate cloth image mask
                    input_image_path = user_clothes_instance.image
                    input_image = cv2.imread(str(input_image_path))
                    result = segment_cloth(input_image)
                    cloth_mask_image = result["cloth_mask_image"]
                    output_folder = "clothMask"
                    os.makedirs(output_folder, exist_ok=True)
                    cloth_image_path = os.path.join(output_folder, "cloth_mask.jpg")
                    cv2.imwrite(cloth_image_path, cloth_mask_image)
                    #error here
                    generated_image = cv2.imread(cloth_image_path)
                    # Convert the numpy array to a byte string
                    generated_image_bytes = cv2.imencode('.jpg', generated_image)[1].tobytes()

                    # Create a ContentFile from the byte string and specify a filename
                    generated_image_file = ContentFile(generated_image_bytes, name='generated_image.jpg')

                    serializer_generated_image = UserGeneratedImageSerializer(data={
                        'user': user.id,
                        'user_image': user_image_instance.id,
                        'user_clothes': user_clothes_instance.id,
                        'generated_image': generated_image_file
                    })
                    if serializer_generated_image.is_valid():
                        user_generated_image_instance = serializer_generated_image.save()
                        return Response(serializer_generated_image.data, status=status.HTTP_201_CREATED)
                    else:
                        return Response(serializer_generated_image.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializerImage.errors, status=status.HTTP_400_BAD_REQUEST)