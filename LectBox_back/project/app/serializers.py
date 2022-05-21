from rest_framework import serializers
from app.models import Users

# 회원가입시 사용
# 유저 모든 정보 포함
class SignUptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['u_id', 'pw', 'is_student', 'name', 'email', 'school', 'department']