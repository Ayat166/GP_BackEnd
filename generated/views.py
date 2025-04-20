import json
import numpy as np
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from cloths.models import UserClothes
from generated.models import UserGeneratedImage
from generated.serializers import UserGeneratedImageSerializer ,UserGeneratedImageSerializerRetrive
from users.models import User
from cloths.serializers import UserImageSerializer , UserClothesImageSerializer
from rest_framework.exceptions import AuthenticationFailed
import jwt
from models.cloth_mask import segment_cloth
import cv2
import os
# Create your views here.
from django.core.files.base import ContentFile
from models.graphonomy_master.exp.inference.inference import inference
from models.VITON_HD.test import test
from PIL import Image, ImageDraw
from io import BytesIO
from models.openpose import create_densepose_image
from gradio_client import Client, file # type: ignore

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
            
            # Generate cloth image mask
            input_image_path = user_clothes_instance.image.path
            print(input_image_path)
            cloth_image = cv2.imread(input_image_path)
            result = segment_cloth(cloth_image)
            cloth_mask_image = result["cloth_mask_image"]

            input_user_image_path = user_image_instance.image.path
            input_user_image = cv2.imread(str(input_user_image_path)) 
            
            
            # Perform inference
            ori_img=cv2.resize(input_user_image,(768,1024))
            img=cv2.resize(ori_img,(384,512))
            

            
            parsing_image, gray_image = inference(img, use_gpu=True)
            densepose_image , openpose_json = create_densepose_image(input_user_image) 
            cloth_image = cv2.cvtColor(cloth_image, cv2.COLOR_BGR2RGB)
            input_user_image = cv2.cvtColor(input_user_image, cv2.COLOR_BGR2RGB)
            gray_image = gray_image.astype(np.uint8)
            densepose_image = cv2.cvtColor(densepose_image, cv2.COLOR_BGR2RGB)
            cloth_image = Image.fromarray(cloth_image)
            input_user_image = Image.fromarray(input_user_image)
            densepose_image = Image.fromarray(densepose_image)
            cloth_mask = Image.fromarray(cloth_mask_image)
            gray_image=cv2.resize(gray_image,(768,1024))
            gray_image = Image.fromarray(gray_image)
            input_user_image.show()
            cloth_image.show()
            densepose_image.show()
            gray_image.show()
            cloth_mask.show()
            
            
            res = test(input_user_image, cloth_image, cloth_mask, densepose_image, gray_image, openpose_json)
            buffer = BytesIO()
            res.save(buffer, format="JPEG")
            image_bytes = buffer.getvalue()
            generated_image_file = ContentFile(image_bytes, name='generated_image.jpg')
            serializer_generated_image = UserGeneratedImageSerializer(data={
                'user': user.id,
                'user_image': user_image_instance.id,
                'user_clothes': user_clothes_instance.id,
                'generated_image': generated_image_file
            }, context={'request': request})

            if serializer_generated_image.is_valid():
                user_generated_image_instance = serializer_generated_image.save()
                return Response(serializer_generated_image.data, status=status.HTTP_200_OK)
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
                return Response({'message': 'User image added to Fav Successfully'}, status=status.HTTP_200_OK)
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
                return Response({'message': 'User image deleted successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
        
        
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        #user = User.objects.filter(id=payload['id']).first()
        user_images = UserGeneratedImage.objects.filter(user_id=payload['id'])
        serializer = UserGeneratedImageSerializerRetrive(user_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    
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
            cloth_image_instance = UserClothes.objects.filter(id=clothimageid).first()
            if cloth_image_instance:
                if cloth_image_instance.user == user :
                    # generate cloth image mask
                    cloth_image = cloth_image_instance.image
                    cloth_image = cv2.imread(str(cloth_image))
                    result = segment_cloth(cloth_image)
                    cloth_mask_image = result["cloth_mask_image"]

                    input_user_image_path = user_image_instance.image.path
                    input_user_image = cv2.imread(str(input_user_image_path)) 
                    
                    
                    # Perform inference
                    ori_img=cv2.resize(input_user_image,(768,1024))
                    img=cv2.resize(ori_img,(384,512))
                    

                    
                    parsing_image, gray_image = inference(img, use_gpu=True)
                    densepose_image , openpose_json = create_densepose_image(input_user_image) 
                    cloth_image = cv2.cvtColor(cloth_image, cv2.COLOR_BGR2RGB)
                    input_user_image = cv2.cvtColor(input_user_image, cv2.COLOR_BGR2RGB)
                    gray_image = gray_image.astype(np.uint8)
                    densepose_image = cv2.cvtColor(densepose_image, cv2.COLOR_BGR2RGB)
                    cloth_image = Image.fromarray(cloth_image)
                    input_user_image = Image.fromarray(input_user_image)
                    densepose_image = Image.fromarray(densepose_image)
                    cloth_mask = Image.fromarray(cloth_mask_image)
                    gray_image = Image.fromarray(gray_image)
                    
                    res = test(input_user_image, cloth_image, cloth_mask, densepose_image, gray_image, openpose_json)
                    buffer = BytesIO()
                    res.save(buffer, format="JPEG")
                    image_bytes = buffer.getvalue()
                    generated_image_file = ContentFile(image_bytes, name='generated_image.jpg')
                    serializer_generated_image = UserGeneratedImageSerializer(data={
                        'user': user.id,
                        'user_image': user_image_instance.id,
                        'user_clothes': cloth_image_instance.id,
                        'generated_image': generated_image_file
                    }, context={'request': request})

                    if serializer_generated_image.is_valid():
                        user_generated_image_instance = serializer_generated_image.save()
                        return Response(serializer_generated_image.data, status=status.HTTP_200_OK)
                    else:
                        return Response(serializer_generated_image.errors, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({'message': 'Unauthorized!'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'message': 'User does not have the specified image'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializerImage.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
class FavouriteGeneratedClothView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        try:
            payload = jwt.decode(token,'secret',algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')
        #user = User.objects.filter(id=payload['id']).first()
        user_images = UserGeneratedImage.objects.filter(user_id=payload['id'], is_fav=True)
        serializer = UserGeneratedImageSerializerRetrive(user_images, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    

class UserGeneratedIDMView(APIView):
    # if IDM API
    def post(self, request):
        try:
            user_image_data = {"image": request.data["user_image"]}
            user_cloth_data = {"image": request.data["user_cloth"]}
        except KeyError:
            return Response({"message": "Both user_image and user_cloth data are required."}, status=status.HTTP_400_BAD_REQUEST)
        
        serializerImage = UserImageSerializer(data=user_image_data)
        serializerClothes = UserClothesImageSerializer(data=user_cloth_data)
        if serializerImage.is_valid() and serializerClothes.is_valid():
            
            user = User.objects.filter(id=3).first()
            user_image_instance = serializerImage.save(user=user)
            user_clothes_instance = serializerClothes.save(user=user)
            
            # Generate cloth image mask
            garment_img_url = user_clothes_instance.image.path
           

            background_url = user_image_instance.image.path
            
            # Initialize the client with your Hugging Face space name
            client = Client("yisol/IDM-VTON")

            # Define parameters as per the API documentation
            result = client.predict(
                dict={"background": file(background_url), "layers": [], "composite": None},
                garm_img=file(garment_img_url),
                garment_des="Hello!!",
                is_checked=True,
                is_checked_crop=False,
                denoise_steps=30,
                seed=42,
                api_name="/tryon"
            )
            print(result[0])
            # Path to the generated image
            generated_image_path = result[0]  # Assuming this is the path to the generated image

            # Open the image from the path
            with Image.open(generated_image_path) as img:
                # Convert the image to a byte buffer
                buffer = BytesIO()
                img.save(buffer, format="JPEG")
                image_bytes = buffer.getvalue()

            # Create a ContentFile for Django
            generated_image_file = ContentFile(image_bytes, name='generated_image.jpg')
            serializer_generated_image = UserGeneratedImageSerializer(data={
                'user': user.id,
                'user_image': user_image_instance.id,
                'user_clothes': user_clothes_instance.id,
                'generated_image': generated_image_file
            }, context={'request': request})

            if serializer_generated_image.is_valid():
                user_generated_image_instance = serializer_generated_image.save()
                return Response(serializer_generated_image.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer_generated_image.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response([serializerImage.errors, serializerClothes.errors], status=status.HTTP_400_BAD_REQUEST)