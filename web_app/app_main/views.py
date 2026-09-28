from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404





def resume(request,id):
    user =get_object_or_404(User,id=id) 
    context = {'user':user}
    return render(request,'resume.html',context)


def index(request):
    users=User.objects.all()
    context = {'users':users}
    return render(request,'index.html',context)


