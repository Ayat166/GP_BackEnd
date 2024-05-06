from django.urls import path 
from .views import UserImageView , UserClothImageView

urlpatterns = [
    path('userImage' , UserImageView.as_view()),
    path('userClothImage' , UserClothImageView.as_view()),
]