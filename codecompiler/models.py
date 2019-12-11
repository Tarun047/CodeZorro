from django.db import models
from django.contrib.auth.models import User

class Code(models.Model):
    source = models.CharField(max_length=5*10**6,default='')
    #user = models.ForeignKey(User,on_delete=models.CASCADE)
    runtimestamp = models.DateTimeField(auto_now_add=True)
    verdict = models.IntegerField(default=0)
    language = models.CharField(max_length=20,default='')
