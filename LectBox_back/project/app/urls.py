from django.urls import path, include
from app import views

urlpatterns = [
    path('sign-up/', views.SignupView.as_view()),
    path('member/', views.user_list),
    path('member-detail/', views.user_detail),
    path('login/', views.LoginView.as_view()),
    path('folder/<int:f_id>', views.folder_detail),
    path('folder/<int:f_id>/<int:type>', views.folder_type),
    path('folder_path/<int:f_id>', views.folder_path),
    path('folder/', views.folder_detail),
    path('class-list/', views.class_list),
    path('class-entrance/<int:f_id>',views.class_entrance),
    path('folder/<int:folder_id>/file/<int:file_id>/', views.FileDetailView.as_view()),
    path('folder/<int:folder_id>/file/', views.FileUploadView.as_view()),
    path('folder/<int:folder_id>/file/<int:file_id>/delete/', views.FileDeleteView.as_view()),
    path('folder/<int:folder_id>/file/<int:file_id>/downloads/', views.FileDownloadView.as_view()),
    path('folder/<int:folder_id>/file/<int:file_id>/url/', views.s3URL),
]