from django.urls import path 
from .views import UserImageView , UserClothImageView

urlpatterns = [
    path('userImage/<str:token>' , UserImageView.as_view()),
    path('userClothImage/<str:token>' , UserClothImageView.as_view()),
    path('userClothImage/all/<str:token>' , UserClothImageView.as_view(), name='user_images'),
    path('userImage/<int:image_id>/<str:token>', UserImageView.as_view(), name='user_image_delete'),
    path('userClothImage/<int:cloth_image_id>/<str:token>', UserClothImageView.as_view(), name='user_cloth_image_delete'),

]