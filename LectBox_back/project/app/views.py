from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser
from app.models import Users
from app.serializers import UserSerializer

from django.shortcuts import render
#from yaml import serialize

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .serializers import UserLoginSerializer

from rest_framework import status

from rest_framework.decorators import api_view

#존재하는 id인지 확인
def isExist(id):
    return User.objects.filter(username=id).exists()


#회원가입
class SignupView(APIView):
    def post(self, request):
        #아이디 중복 검사
        if(isExist(request.data['id'])):
            return Response({"이미 존재하는 id"},status=403)
        #회원정보 저장    
        user = User.objects.create_user(username=request.data['id'], password=request.data['pw'])
        users = Users(user=user, is_student=request.data['is_student'] , name=request.data['name'], email=request.data['email'], school=request.data['school'], department=request.data['department'])
        user.save()
        users.save()

        return Response({"ok"},status=200)

        '''
        #회원 가입과 로그인이 동시 진행 되는 경우
        token = Token.objects.create(user=user)
        return Response({"Token": token.key})
        '''
#로그인
class LoginView(APIView):
    def post(self, request):
        user = authenticate(username=request.data['id'], password=request.data['pw'])
        if user is not None:
            token = Token.objects.create(user=user)
            #token = Token.objects.get(user=user)
            return Response({"Token": token.key}, status=200)
        else:
            return Response({"'id 또는 pw가 일치하지 않습니다."},status=401)

@csrf_exempt
@api_view(['POST'])
def user_list(request):
    """
    유저 전체 정보 이용
    """
    #유저 데이터 삽입여부 테스트용
    if request.method == 'GET':
        user = Users.objects.all()
        serializer = UserSerializer(user, many =True)
        return JsonResponse(serializer.data, safe=False)
       
    

@csrf_exempt
@api_view(['GET','PUT', 'DELETE'])
def user_detail(request):
    """
    특정 유저 정보 이용
    """
    try:
        user = User.objects.get(username=request.user)
    except Users.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)

    #유저 정보 획득
    if request.method == 'GET':
        return Response({"id": user.username, "is_student": users.is_student, "name":users.name, "email":users.email, "school":users.school, "department":users.department}, status=200)

'''
    #유저 정보 수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = SnippetSerializer(snippet, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    #유저 정보 삭제(회원 탈퇴)
    elif request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)
'''



