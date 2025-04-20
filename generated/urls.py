from django.urls import path
from .views import UserGeneratedView ,UserGeneratedWithClothView ,FavouriteGeneratedClothView ,UserGeneratedIDMView

urlpatterns = [
    path('user-generated-image', UserGeneratedView.as_view(), name='user_generated_image'),
    path('user-generated-image/addfav/<int:FavId>', UserGeneratedView.as_view(), name='user_generated_image_Fav'),
    path('user-generated-image/cloth/<int:clothimageid>', UserGeneratedWithClothView.as_view(), name='user_generated_image_withcloth_exists'),
    path('user-generated-image/delete/<int:imageId>', UserGeneratedView.as_view(), name='user_generated_image_Delete'),
    path('user-generated-image/all',UserGeneratedView.as_view(),name='all_user_generated'),
    path('user-generated-image/allFav',FavouriteGeneratedClothView.as_view(),name='all_Fav_user_generated'),
    path('user-generated-image/IDM', UserGeneratedIDMView.as_view(), name='user_generated_image_idm'),

]
