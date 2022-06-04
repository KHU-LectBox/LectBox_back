from rest_framework import serializers
from app.models import User, Users, FolderItems, Folder_User_Relationships, Folder_File_Relationships

from rest_framework import serializers
from django.contrib.auth.models import User

from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token

class childSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Folder_File_Relationships
        fields = ['parent', 'child', 'name', 'is_folder', 'child_type']

class FolderSerializer(serializers.ModelSerializer):

    #items = serializers.

    class Meta:
        model = FolderItems
        fields = ['id', 'made_by', 'name', 'max_volume', 'volume', 'type']

# 유저 모든 정보 포함
class UserSerializer(serializers.ModelSerializer):
    
    def update(self, instance, validated_data):
        instance.is_student = validated_data.get('is_student',instance.is_student)
        instance.name = validated_data.get('name',instance.name)
        instance.email = validated_data.get('email',instance.email)
        instance.school = validated_data.get('school',instance.school)
        instance.department = validated_data.get('department',instance.department)
        instance.save()
        return instance
    
    class Meta:
        model = Users
        fields = ['user', 'is_student', 'name', 'email', 'school', 'department']

class FSerializer(serializers.ModelSerializer):

    #items = serializers.
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name',instance.name)
        instance.save()
        return instance

    class Meta:
        model = FolderItems
        fields = ['id', 'made_by', 'name', 'max_volume', 'volume', 'type']

class FUSerializer(serializers.ModelSerializer):

    class Meta:
        model = Folder_User_Relationships
        fields = ['folder_id', 'user_id','type']

class ClassSerializer(serializers.ModelSerializer):
    #class list
    class Meta:
        model = FolderItems
        fields = ['id', 'made_by', 'name']

