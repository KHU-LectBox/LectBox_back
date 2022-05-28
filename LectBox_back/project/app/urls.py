from django.urls import path, include
from app import views

urlpatterns = [
    path('sign-up/', views.SignupView.as_view()),
    path('member-detail/', views.user_detail),
    path('login/', views.LoginView.as_view()),
]

#유저 id 파라미터로 받는 형식
#path('users/<str:userid>', views.user_detail)