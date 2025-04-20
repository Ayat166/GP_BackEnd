from django.urls import path 
from .views import RegisterView , LoginView ,UserView , LogoutView

urlpatterns = [
    path('register' , RegisterView.as_view()),
    path('login' , LoginView.as_view()),
    path('user/<str:token>' , UserView.as_view()),
    path('logout/<str:token>' , LogoutView.as_view()),
]