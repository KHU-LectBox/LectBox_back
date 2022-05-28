from rest_framework import serializers
from app.models import Users

from rest_framework import serializers
from django.contrib.auth.models import User
from app.models import Users

from django.contrib.auth.models import update_last_login
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token



# 유저 모든 정보 포함
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['user.username', 'user.password', 'is_student', 'name', 'email', 'school', 'department']


def ttt(username, password):
    user = Users.objects.filter(username = username).filter(password= password)
    return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20)
    password = serializers.CharField(max_length=20, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        id = data.get("id", None)
        password = data.get("pw", None)
        user = authenticate(username=id, password=password)
        print(f'로그인 성공? : {user}')
        if user is None:
            return {
                'id': 'None'
            }
        try:
            #update_last_login(None, user)
            token = Token.objects.get_or_create(user=user)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                'User with given id and password does not exists'
            )
        return {
            'id': user.username,
            'token': token
        }