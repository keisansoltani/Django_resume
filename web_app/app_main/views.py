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
    q = request.GET.get('q', '')
    skills = request.GET.getlist('skill')
    degree = request.GET.get('degree', '')
    major = request.GET.get('major', '')
    users = User.objects.all()

    if q:
        users = users.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(skills__name__icontains=q)
        )

    if skills:
        for s in skills:
            users = users.filter(skills__name=s)

    if degree:
        users = users.filter(profile__education=degree)

    if major:
        users = users.filter(profile__description=major)

    users = users.distinct().order_by('id')


    items_per_page = 9
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'q': q, 'skills': skills, 'degree': degree, 'major': major}
    return render(request, "index.html", context)









