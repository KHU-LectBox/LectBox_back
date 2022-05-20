from django.urls import path, include
from app import views

urlpatterns = [
    path('sign-up/', views.user_list),
    path('users/<str:userid>', views.user_detail),
]