from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .models import User
import jwt
import datetime
from rest_framework import status

# Create your views here.

class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Validation errors', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        if not email or not password:
            return Response({'message': 'Email and password are required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.filter(email=email).first()
        
        if user is None:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        
        if not user.check_password(password):
            return Response({'message': 'Incorrect password!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret', algorithm='HS256')
        
        respone = Response()
        respone.set_cookie(key='jwt',value=token,httponly=True)
        respone.data = {
            'jwt':token
        }
        respone.status_code = status.HTTP_200_OK
        return respone
    
class UserView(APIView):
    def get(self, request, token):
        if not token:
            return Response({'message': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, token):
        if not token:
            return Response({'message': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        user = User.objects.filter(id=payload['id']).first()
        if not user:
            return Response({'message': 'User not found!'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserSerializer(user, data=request.data, context={'request': request})
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response({'message': 'Validation errors', 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
      
class LogoutView(APIView):
    def post(self, request, token):
        try:
            # Decode the token to ensure it's valid before attempting to delete it
            jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            return Response({'message': 'Unauthenticated!'}, status=status.HTTP_401_UNAUTHORIZED)
        except jwt.InvalidTokenError:
            return Response({'message': 'Invalid token!'}, status=status.HTTP_401_UNAUTHORIZED)
        
        response = Response()
        # Optionally, clear the token cookie if it exists
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out'
        }
        response.status_code = status.HTTP_200_OK
        return response
