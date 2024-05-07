from django.urls import path
from .views import UserGeneratedView

urlpatterns = [
    path('user-generated-image/', UserGeneratedView.as_view(), name='user_generated_image'),
]
