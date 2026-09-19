from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50)
    education=models.CharField(max_length=50,null=True)
    description=models.TextField(null=True)
    


class experience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    details=models.TextField()
    
