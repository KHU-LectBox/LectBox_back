from django.urls import path, include
from app import views

urlpatterns = [
    path('sign-up/', views.SignupView.as_view()),
    path('member-detail/', views.user_detail),
    path('login/', views.LoginView.as_view()),
    path('folder/<int:f_id>', views.folder_detail),
    path('folder/<int:f_id>/<int:type>', views.folder_type),
    path('folder_path/<int:f_id>', views.folder_path),
    path('folder/', views.folder_detail),
    path('class-list/', views.class_list),
    path('class-entrance/<int:f_id>',views.class_entrance),
  
]
