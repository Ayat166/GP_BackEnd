from django.urls import path
from .views import UserGeneratedView

urlpatterns = [
    path('user-generated-image/', UserGeneratedView.as_view(), name='user_generated_image'),
    path('user-generated-image/<int:FavId>/', UserGeneratedView.as_view(), name='user_generated_image_Fav'),
    path('user-generated-image/delete/<int:imageId>/', UserGeneratedView.as_view(), name='user_generated_image_Delete'),
]
