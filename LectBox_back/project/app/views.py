
import base64
from django.http import FileResponse

##
from pickle import TRUE
import string
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.parsers import JSONParser

from app.models import User, Users, FolderItems, Folder_User_Relationships, Folder_File_Relationships, File
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

import boto3
import botocore
import os
from pathlib import Path
import json

CLASS_MAX_VOLUME = 250*1000

#존재하는 id인지 확인
def isExist(id):
    return User.objects.filter(username=id).exists()

#volume값이 지정된 child_id 넣으면 그 부모 폴더들의 volume값에 addvolume이 더해지며 수정된다.
def UpdateVolume(child_id, is_folder, addvolume):

    print(f'추가된 볼륨:{addvolume}')
    target = child_id
    isEnd = False
    
    if(is_folder == True):
        child = FolderItems.objects.get(id = target)
    else:
        child = File.objects.get(id = target)

    try:
        parent_folder = Folder_File_Relationships.objects.filter(is_folder=False).get(child= child.id)
        folder = FolderItems.objects.get(id = parent_folder.parent.id)

        parent_folder.child_volume = parent_folder.child_volume + addvolume
        parent_folder.save()
        folder.volume = folder.volume + addvolume
        folder.save()
        print(f'수정된 볼륨{folder.volume}')

    except Folder_File_Relationships.DoesNotExist:
        isEnd = True

    while(not isEnd):
        try:
            parent_folder = Folder_File_Relationships.objects.filter(is_folder=True).get(child= folder.id)
            folder = FolderItems.objects.get(id = parent_folder.parent.id)

            parent_folder.child_volume = parent_folder.child_volume + addvolume
            parent_folder.save()
            folder.volume = folder.volume + addvolume
            folder.save()
            print(f'수정된 볼륨: {folder.name}')
        except Folder_File_Relationships.DoesNotExist:
            isEnd = True
            break
        
    return True


#회원가입
class SignupView(APIView):
    def post(self, request):
        #아이디 중복 검사
        if(isExist(request.data['id'])):
            return Response({"duplicated id"},status=403)
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
            #token = Token.objects.get_or_create(user=user)
            token, created = Token.objects.get_or_create(user=user)
            print(token.key)
            users = Users.objects.get(user= user)
            return Response({"Token": token.key, "id":user.username, "name" : users.name, "is_student" : users.is_student }, status=200)
        else:
            return Response({"'id 또는 pw가 일치하지 않습니다."},status=401)

@csrf_exempt
@api_view(['GET'])
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
def folder_detail(request, f_id = None):
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
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": (folder.max_volume/1000), "volume": (folder.volume/1000), "type": folder.type, 'items':serialized_items.data}, status=200)
        else:
            items = None
            return Response({"id": folder.id, "made_by": folder.made_by.username , "name": folder.name, "max_volume": (folder.max_volume/1000), "volume": (folder.volume/1000), "type": folder.type, 'items':items}, status=200)
        
        
    #폴더 생성
    if request.method == 'POST':
        folder = FolderItems(made_by=request.user, name=request.data['name'],max_volume=CLASS_MAX_VOLUME ,volume= 0,type=request.data['type'])
        folder.save()

        #부모폴더가 있는 경우 Folder_File_Relationships에 튜플 생성
        if(not (request.data['parent'] == 0)):
            
            p_folder = FolderItems.objects.get(id =int(request.data['parent']))
            relation = Folder_File_Relationships(parent =p_folder, child =folder.id, name=request.data['name'],is_folder=True,child_type = request.data['type'], child_volume=0, child_made_by_name = users.name)
            relation.save()
        folder_user = Folder_User_Relationships(folder_id=folder.id, user_id=user.username,type=folder.type)
        folder_user.save()

        #강의실 생성시 자동으로 강의,과제 폴더 생성
        if((request.data['type'] == 0) or (request.data['type'] == '0') ):
            #생성한 폴더가 곧 부모폴더
            p_folder = FolderItems.objects.get(id =folder.id)

            #강의
            Lecture_folder = FolderItems(made_by=request.user, name='Lecture',max_volume=100,volume= 0,type='1')
            Lecture_folder.save()
            Lecture_relation = Folder_File_Relationships(parent =p_folder, child =Lecture_folder.id, name=Lecture_folder.name,is_folder=True,child_type = Lecture_folder.type, child_volume=0, child_made_by_name = users.name)
            Lecture_relation.save()
            Lecture_user = Folder_User_Relationships(folder_id=Lecture_folder.id, user_id=user.username,type=Lecture_folder.type)
            Lecture_user.save()

            #과제
            Assignment_folder = FolderItems(made_by=request.user, name='Assignment',max_volume=100,volume= 0,type='2')
            Assignment_folder.save()
            Assignment_relation = Folder_File_Relationships(parent =p_folder, child =Assignment_folder.id, name=Assignment_folder.name,is_folder=True,child_type = Assignment_folder.type, child_volume=0, child_made_by_name = users.name)
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
def folder_type(request, f_id = None, type=None):
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
            items = None
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
                parent_folder = Folder_File_Relationships.objects.filter(is_folder=True).get(child= folder.id)
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
def class_list(request, f_id = None):
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
        print(f'결과:{result}')
        
    jsondata = json.dumps(result)#serializers.serialize('json', result)# fields=('id','made_by','name'))
    return Response({jsondata}, status=200)
    #return Response({'class-list' : jsondata}, status=200)
    #return JsonResponse({'query_set'})

#강의실 입장
@csrf_exempt
@api_view(['GET'])
def class_entrance(request,f_id=None):
    """
    using popup, enter the class
    """
    try:
        user = User.objects.get(username=request.user)
    except User.DoesNotExist:
        return HttpResponse(status=404)
    users = Users.objects.get(user = user)

    folder = get_object_or_404(FolderItems, id = f_id)

    if(not (folder.type == '0' or folder.type == 0)):
        return Response({'강의실이 아닙니다'}, status=404)

    folder_user = Folder_User_Relationships(folder_id=folder.id, user_id=user.username, type='0')
    folder_user.save()

    return Response({'폴더생성성공'}, status=200)

BASE_DIR = Path(__file__).resolve().parent.parent


def connect_s3():
        secret_file = os.path.join(BASE_DIR, 'secrets.json')
        with open(secret_file) as f:
            secrets = json.loads(f.read())
            try:
                AWS_ACCESS_KEY_ID = secrets['AWS_ACCESS_KEY_ID']
                AWS_SECRET_ACCESS_KEY = secrets['AWS_SECRET_ACCESS_KEY']
                AWS_BUCKET_NAME = secrets['AWS_BUCKET_NAME']
                AWS_S3_BASE_DIR = secrets['AWS_S3_BASE_DIR']
                AWS_S3_REGION_NAME = secrets['AWS_S3_REGION_NAME']
            except KeyError:
                raise KeyError('No Keys found in secrets.json')

        s3 = boto3.resource('s3', aws_access_key_id = AWS_ACCESS_KEY_ID, aws_secret_access_key = AWS_SECRET_ACCESS_KEY)

        return s3, AWS_BUCKET_NAME, AWS_S3_BASE_DIR, AWS_S3_REGION_NAME

# Create your views here.
class FileDetailView(APIView):
    s3, aws_bucket_name, aws_s3_base_dir, aws_s3_region_name = connect_s3()

    def get(self, request, folder_id, file_id):
        path = '{}/{}/{}'.format(self.aws_s3_base_dir, folder_id, file_id)

        # Check if the user not logged in
        if not request.user:
            return Response({'User not login'}, status=401)
        
        # Check if the file object exists
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({'File object does not exist'}, status=404)
        
        # # Check if the file exists in the bucket
        # if not self.s3.meta.client.list_objects_v2(Bucket=self.aws_bucket_name, Prefix=path):
        #     return Response({'File does not exist in the bucket'}, status=404)
        
        return Response({'f_id' : file.id, 'name' : file.name, 'created_at' : file.created_at, 'volume' : file.volume}, status=200)


class FileUploadView(APIView):
    s3, aws_bucket_name, aws_s3_base_dir, aws_s3_region_name = connect_s3()
        
    def post(self, request, folder_id):
        path = '{}/{}/file/{}'.format(self.aws_s3_base_dir, folder_id, request.FILES['file'].name)

        # Check if the user not logged in
        try:
            user = User.objects.get(username=request.user)
            
        except User.DoesNotExist:
            return Response({'User not login'}, status=401)
        users=Users.objects.get(user=user)
        # Upload the file to the bucket
        try:
            self.s3.meta.client.upload_fileobj(request.FILES['file'], self.aws_bucket_name, path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return Response({'File does not exist'}, status=404)
            else:
                return Response({'File upload failed'}, status=400)

        # Mapping to file model
        file = File(
            # file=request.FILES['file'],
            made_by=user,
            name=request.FILES['file'].name, 
            volume=int((request.FILES['file'].size)/1000),
            is_protected=request.POST.get('is_protected', False)) #request.data['is_protected'])
        file.save()
        
        p_folder = FolderItems.objects.get(id =int(folder_id))
        relation = Folder_File_Relationships(parent =p_folder, child =file.id, name=file.name,is_folder=False,child_type = p_folder.type, child_volume=file.volume, child_made_by_name = users.name)
        relation.save()
        print(f'파일의 볼륨: {file.volume}')
        UpdateVolume(file.id, False, file.volume) # 볼륨수정


        return Response({'file_id':file.id}, status=200)


class FileDeleteView(APIView):
    s3, aws_bucket_name, aws_s3_base_dir, aws_s3_region_name = connect_s3()

    def delete(self, request, folder_id, file_id):
        

        # Check if the user not logged in
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return HttpResponse(status=404)
    
        users = Users.objects.get(user = user)

        # Check if the file object exists
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({'File object does not exist'}, status=404)

        path = '{}/{}/file/{}'.format(self.aws_s3_base_dir, folder_id, file.name)
        
        # Check if the file exists in the bucket
        if not self.s3.meta.client.list_objects_v2(Bucket=self.aws_bucket_name, Prefix=path):
            return Response({'File does not exist in the bucket'}, status=404)
        
        # Check if the user has permission to delete the file
        if file.is_protected and (user != file.made_by and users.is_student):
            return Response({'User does not have permission to delete the file'}, status=401)
        
        # Delete the file from the bucket
        try:
            self.s3.Object(self.aws_bucket_name, path).delete()
        except botocore.exceptions.ClientError as e:
            return Response({'Delete file from the bucket failed'}, status=400)
        
        relation = Folder_File_Relationships.objects.get(parent =int(folder_id), child =file.id)

        #UpdateVolume(file.id, False, -1*file.volume) # 볼륨수정

        relation.delete()
        file.delete()
        
        return Response({'File deleted'}, status=200)

class FileDownloadView(APIView):
    s3, aws_bucket_name, aws_s3_base_dir, aws_s3_region_name = connect_s3()

    def get(self, request, folder_id, file_id):
        # Check if the user not logged in
        try:
            user = User.objects.get(username=request.user)
        except User.DoesNotExist:
            return HttpResponse(status=404)

        users = Users.objects.get(user = user)

        # Check if the file object exists
        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({'File object does not exist'}, status=404)

        path = '{}/{}/file/{}'.format(self.aws_s3_base_dir, folder_id, file.name)

        # Check if the file exists in the bucket
        if not self.s3.meta.client.list_objects_v2(Bucket=self.aws_bucket_name, Prefix=path):
            return Response({'File does not exist in the bucket'}, status=404)

        # Check if the user has permission to delete the file
        if file.is_protected and (user != file.made_by and users.is_student):
            return Response({'User does not have permission to delete the file'}, status=401)

        # Download the file from the bucket
        try:
            with open('./'+file.name, 'wb') as data:
                self.s3.meta.client.download_fileobj(self.aws_bucket_name, path, data)
            with open('./'+file.name, 'rb') as data:
                #컨텐츠타입 지정
                return HttpResponse(data.read(), content_type="image/png")
            
            '''
                #base64인코딩해서보내기
                #target = data.read()
                target = base64.b64encode(data.read())
            os.remove('./'+file.name)
            return Response(target,status=200)
            #self.s3.meta.client.download_file(self.aws_bucket_name, path, file.name)
            '''
                
            '''
            바이너리파일 보내기
                response = FileResponse(data.read())
                return response
            '''            
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                return Response({'File does not exist in the bucket'}, status=404)
            else:
                return Response({'Error'}, status=400)


@csrf_exempt
@api_view(['GET', 'post', 'PUT', 'DELETE'])
def s3URL(request, folder_id, file_id):
    s3, aws_bucket_name, aws_s3_base_dir, aws_s3_region_name = connect_s3()
    try:
        user = User.objects.get(username=request.user)
    except Users.DoesNotExist:
        return HttpResponse(status=404)
    
    users = Users.objects.get(user = user)
    if request.method == 'GET':

        try:
            file = File.objects.get(id=file_id)
        except File.DoesNotExist:
            return Response({'File object does not exist'}, status=404)

        path = '{}/{}/file/{}'.format(aws_s3_base_dir, folder_id, file.name)

        # Check if the file exists in the bucket
        if not s3.meta.client.list_objects_v2(Bucket=aws_bucket_name, Prefix=path):
            return Response({'File does not exist in the bucket'}, status=404)
    result = 'https://s3.ap-northeast-2.amazonaws.com/'+ aws_bucket_name +'/'+path
    return Response({result})
