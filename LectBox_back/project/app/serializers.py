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

