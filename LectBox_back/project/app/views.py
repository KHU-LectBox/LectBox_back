from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from app.models import Users
from app.serializers import SignUptSerializer

@csrf_exempt
def user_list(request):
    """
    유저 전체 정보 이용
    """
    # 회원 가입
    if request.method == 'POST':
        data = JSONParser().parse(request)
        print("log01")
        print(data)
        serializer = SignUptSerializer(data= data)
        print("log02")
        if serializer.is_valid():
            print("log03")
            serializer.save()
            print("log04")
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)
    
    #데이터 삽입여부 테스트용
    if request.method == 'GET':
        user = Users.objects.all()
        serializer = SignUptSerializer(user, many =True)
        return JsonResponse(serializer.data, safe=False)
       
    

@csrf_exempt
def user_detail(request, userid):
    """
    특정 유저 정보 이용
    """
    try:
        user = Users.objects.get(u_id=userid)
    except Users.DoesNotExist:
        return HttpResponse(status=404)

    #유저 정보 획득
    if request.method == 'GET':
        serializer = SignUptSerializer(user)
        return JsonResponse(serializer.data)

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