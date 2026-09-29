from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q





def resume(request,id):
    user =get_object_or_404(User,id=id) 
    context = {'user':user}
    return render(request,'resume.html',context)


def index(request):
    q = request.GET.get('q')
    if q:
        users=User.objects.filter(
        Q(first_name__icontains=q)|
        Q(last_name__icontains=q)|
        Q(skills__name__icontains=q)
        ).distinct()
    else:
        users=User.objects.all()
    items_per_page = 9
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context={'page_obj':page_obj,'q':q}
    return render(request, "index.html", context)









