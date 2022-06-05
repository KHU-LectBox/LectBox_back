from asyncio.windows_events import NULL
from pickle import TRUE
import string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser

from app.models import User, Users, FolderItems, Folder_User_Relationships, Folder_File_Relationships
from app.serializers import childSerializer, UserSerializer, ClassSerializer

from django.shortcuts import render, get_object_or_404
from django.forms.models import model_to_dict
import json
#from yaml import serialize

# Create your views here.
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from rest_framework import status

from rest_framework.decorators import api_view

from django.core import serializers

#존재하는 id인지 확인
def isExist(id):
    return User.objects.filter(username=id).exists()


#회원가입
class SignupView(APIView):
    def post(self, request):
        #아이디 중복 검사
        if(isExist(request.data['id'])):
            return Response({"duplicated id"},status=200)
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
        print(request.data)
        user = authenticate(username=request.data['id'], password=request.data['pw'])
        if user is not None:
            #token = Token.objects.get_or_create(user=user)
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            users = Users.objects.get(user= user)
            return Response({"Token": token.key, "id":user.username, "name" : users.name, "is_student" : users.is_student }, status=200)
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
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)

    #유저 정보 획득
    if request.method == 'GET':
        return Response({"id": user.username, "is_student": users.is_student, "name":users.name, "email":users.email, "school":users.school, "department":users.department}, status=200)

    #유저 정보 수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = UserSerializer(users,data)
        if serializer.is_valid():
            serializer.save() #db에저장해야함
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    #유저 정보 삭제(회원 탈퇴)
    elif request.method == 'DELETE':
        user.delete()
        users.delete()
        return HttpResponse(status=204)

@csrf_exempt
@api_view(['GET', 'post', 'PUT', 'DELETE'])
def folder_detail(request, f_id = NULL):
    """
    폴더 정보를 받는다.
    """
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)


    #폴더정보 요청
    if request.method == 'GET':
        #폴더 결정
        folder = FolderItems.objects.get(id = f_id)
        
        #자식 폴더 결정
        if (Folder_File_Relationships.objects.filter(parent = f_id).exists()):
            items = Folder_File_Relationships.objects.filter(parent = f_id)
            serialized_items = childSerializer(items, many=True)
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": folder.max_volume, "volume": folder.volume, "type": folder.type, 'items':serialized_items.data}, status=200)
        else:
            items = NULL
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": folder.max_volume, "volume": folder.volume, "type": folder.type, 'items':items}, status=200)
        
        
    #폴더 생성
    if request.method == 'POST':
        folder = FolderItems(made_by=request.user, name=request.data['name'],max_volume=100,volume= 0,type=request.data['type'])
        folder.save()

        #부모폴더가 있는 경우 Folder_File_Relationships에 튜플 생성
        if(not (request.data['parent'] == 0)):
            
            p_folder = FolderItems.objects.get(id =int(request.data['parent']))
            relation = Folder_File_Relationships(parent =p_folder, child =folder.id, name=request.data['name'],is_folder=True,child_type = request.data['type'])
            relation.save()
        folder_user = Folder_User_Relationships(folder_id=folder.id, user_id=user.username,type=folder.type)
        folder_user.save()

        #강의실 생성시 자동으로 강의,과제 폴더 생성
        if(request.data['type'] == '0'):
            #생성한 폴더가 곧 부모폴더
            p_folder = FolderItems.objects.get(id =folder.id)

            #강의
            Lecture_folder = FolderItems(made_by=request.user, name='Lecture',max_volume=100,volume= 0,type='1')
            Lecture_folder.save()
            Lecture_relation = Folder_File_Relationships(parent =p_folder, child =Lecture_folder.id, name=Lecture_folder.name,is_folder=True,child_type = Lecture_folder.type)
            Lecture_relation.save()
            Lecture_user = Folder_User_Relationships(folder_id=Lecture_folder.id, user_id=user.username,type=Lecture_folder.type)
            Lecture_user.save()

            #과제
            Assignment_folder = FolderItems(made_by=request.user, name='Assignment',max_volume=100,volume= 0,type='2')
            Assignment_folder.save()
            Assignment_relation = Folder_File_Relationships(parent =p_folder, child =Assignment_folder.id, name=Assignment_folder.name,is_folder=True,child_type = Assignment_folder.type)
            Assignment_relation.save()
            Assignment_user = Folder_User_Relationships(folder_id=Assignment_folder.id, user_id=user.username,type=Assignment_folder.type)
            Assignment_user.save()

        return Response({'id': folder.id, }, status=200)
        
'''
    #폴더 정보 수정
    elif request.method == 'PUT':
        data = JSONParser().parse(request)
        serializer = FSerializer(users,data)
        if serializer.is_valid():
            serializer.save() #db에저장해야함
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    #폴더 정보 삭제
    elif request.method == 'DELETE':
        folder = FolderItems.objects.get(id = f_id)
        folder.delete()
        return HttpResponse(status=204)
'''

@csrf_exempt
@api_view(['GET', 'post', 'PUT', 'DELETE'])
def folder_type(request, f_id = NULL, type=NULL):
    """
    자식이 특정 타입인 폴더 정보를 받는다.
    """
    try:
        user = User.objects.get(username=request.user)
    except Users.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)
    if request.method == 'GET':

        #폴더 결정
        folder = FolderItems.objects.get(id = f_id)
            
        #자식 폴더 결정
        if (Folder_File_Relationships.objects.filter(parent = f_id).exists()):
            items = Folder_File_Relationships.objects.filter(parent = f_id).filter(child_type = type)
            serialized_items = childSerializer(items, many=True)
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": folder.max_volume, "volume": folder.volume, "type": folder.type, 'items':serialized_items.data}, status=200)
        else:
            items = NULL
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": folder.max_volume, "volume": folder.volume, "type": folder.type, 'items':items}, status=200)


#폴더 경로
@csrf_exempt
@api_view(['GET', 'post', 'PUT', 'DELETE'])
def folder_path(request, f_id):
    """
    폴더의 경로를 반환한다.
    """
    
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)
    
    
    if request.method == 'GET':

        folder_list=[]

        target = f_id
        isEnd = False
        folder = FolderItems.objects.get(id = target)
        folder_list.append(folder.name)
        while(not isEnd):
            try:
                parent_folder = Folder_File_Relationships.objects.get(child= folder.id)
                folder = FolderItems.objects.get(id = parent_folder.parent.id)

            except Folder_File_Relationships.DoesNotExist:
                isEnd = True
                break

            folder_list.append(folder.name)

        #경로
        result_path= ""
        for i in range(len(folder_list)-1,-1,-1 ):
            if(i == len(folder_list)-1):
                result_path = result_path + folder_list[i]
            else:
                result_path = result_path +'>'+ folder_list[i]
        #강의실
        result_class = folder_list[len(folder_list)-1]
        
        return Response({"class": result_class, "path": result_path}, status=200)
        
#강의실 리스트
@csrf_exempt
@api_view(['GET'])
def class_list(request, f_id = NULL):
    """
    main page
    """
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    users = Users.objects.get(user = user)
    queryset= Folder_User_Relationships.objects.filter(user_id=user.username,type=0).values('folder_id') #('folder_id','folder_id.made_by','folder_id.name')
    print(f'강의실목록:{queryset}')
    result=[]
    for i in queryset:
        folder = FolderItems.objects.get(id = i['folder_id'])
        dict_obj = model_to_dict( folder )
        print(folder)
        result.append(dict_obj)
        print(result)
        
    jsondata = json.dumps(result)#serializers.serialize('json', result)# fields=('id','made_by','name'))
    return Response({'class-list' : jsondata}, status=200)
    #return JsonResponse({'query_set'})

#강의실 입장
@csrf_exempt
@api_view(['GET'])
def class_entrance(request,f_id=NULL):
    """
    using popup, enter the class
    """
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    users = Users.objects.get(user = user)

    folder = get_object_or_404(FolderItems, id = f_id)

    folder_user = Folder_User_Relationships(folder_id=folder.id, user_id=user.username, type='0')
    folder_user.save()

    return Response({'폴더생성성공'}, status=200)