from django.urls import path 
from .views import UserImageView , UserClothImageView

urlpatterns = [
    path('userImage' , UserImageView.as_view()),
    path('userClothImage' , UserClothImageView.as_view()),
    path('userImage/<int:image_id>/', UserImageView.as_view(), name='user_image_delete'),
    path('userClothImage/<int:cloth_image_id>/', UserClothImageView.as_view(), name='user_cloth_image_delete'),

]