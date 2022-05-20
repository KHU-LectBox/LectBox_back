from django.db import models


class Users(models.Model):
    user_id = models.CharField(max_length=20,blank=False, null= False, unique=True, primary_key=True)
    pw = models.CharField(max_length=20,blank=False, null= False)
    is_student = models.BooleanField(blank=False, null=False)
    name = models.CharField(max_length=20,blank=False, null= False)
    email = models.TextField(blank=False, null= False)
    school = models.TextField(blank=False, null= False)
    department = models.TextField(blank=False, null= False)

    class Meta:
        ordering = ['user_id']
