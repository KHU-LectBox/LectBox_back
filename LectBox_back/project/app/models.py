from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

#유저정보
# user모델의 username, password 사용
class Users(models.Model):
    user = models.OneToOneField(User, null=True ,  on_delete=models.CASCADE)

    is_student = models.BooleanField(blank=False, null=False)
    name = models.CharField(max_length=20,blank=False, null= False)
    email = models.TextField(blank=False, null= False)
    school = models.TextField(blank=False, null= False)
    department = models.TextField(blank=False, null= False)


CLASS_ROOM = 0
LECTURE = 1
ASSIGNMENT = 2
#폴더정보
# user모델의 username, password 사용
class FolderItems(models.Model):
    
    FOLDER_TYPE = (
    ('0','CLASS_ROOM'),
    ('1','LECTURE'), 
    ('2','ASSIGNMENT'),
    )

    #id 자동생성
    made_by = models.ForeignKey(User, related_name="make", on_delete=models.CASCADE, db_column="made_by", to_field="username")
    name = models.TextField(blank=False, null= False)
    max_volume = models.PositiveIntegerField(blank=False, null= False)
    volume = models.PositiveIntegerField(blank=False, null= False)
    type = models.CharField(max_length=1,choices=FOLDER_TYPE, default=LECTURE, null=False)

    '''
    def get_absolute_url(self):
        """Returns the url to access a detail record for this member."""
        return reverse('folder-detail', args=[str(self.id)])
    '''
    class Meta:
        ordering = ['id']


#child 외래키 지정 불가 이슈 해결 필요
#선택지 1) child 2개두고 null허용하던가
#선택지 2) 코딩 섬세하게 해서 삭제시 문제 없게 하던가
class Folder_File_Relationships(models.Model):
    
    FOLDER_TYPE = (
    ('0','CLASS_ROOM'),
    ('1','LECTURE'), 
    ('2','ASSIGNMENT'),
    )
    
    #id 자동생성
    parent = models.ForeignKey("app.FolderItems", related_name="have", on_delete=models.CASCADE, db_column="parent")
    child = models.PositiveIntegerField(blank=False, null= False)
    name = models.TextField(blank=False, null= False)
    is_folder = models.BooleanField(blank=False, null=False)
    child_type = models.CharField(max_length=1,choices=FOLDER_TYPE, default=LECTURE, null=True)
    
    
    def get_absolute_url(self):
        """Returns the url to access a detail record for this member."""
        return reverse('folder-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['id']

class Folder_User_Relationships(models.Model):
    #id 자동생성
    folder_id = models.ForeignKey("app.FolderItems", related_name="match", on_delete=models.CASCADE, db_column="folder_id")
    user_id = models.ForeignKey(User, related_name="match", on_delete=models.CASCADE, db_column="user_id", to_field='username')

 
    def get_absolute_url(self):
        """Returns the url to access a detail record for this member."""
        return reverse('folder-detail', args=[str(self.id)])
    
    class Meta:
        ordering = ['folder_id']
    









