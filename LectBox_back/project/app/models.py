from django.db import models
from django.contrib.auth.models import User

#from rest_framework.authtoken.models import Token


class Users(models.Model):
    user = models.OneToOneField(User, null=True ,  on_delete=models.CASCADE)

    is_student = models.BooleanField(blank=False, null=False)
    name = models.CharField(max_length=20,blank=False, null= False)
    email = models.TextField(blank=False, null= False)
    school = models.TextField(blank=False, null= False)
    department = models.TextField(blank=False, null= False)


#u_id = models.CharField(max_length=20,blank=False, null= False, unique=True, primary_key= True)
#pw = models.CharField(max_length=20,blank=False, null= False)

#토큰
#token = Token.objects.create(user=User)
