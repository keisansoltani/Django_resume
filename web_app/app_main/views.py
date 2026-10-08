from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from .forms import (
    UserUpdateForm,
    ProfileUpdateForm,
    SkillFormSet,
    ExperienceFormSet,
    RoadmapFormSet,
)


def resume_edit(request):
    profile = request.user.profile

    if request.method == 'POST':
        userUpdateForm = UserUpdateForm(request.POST, instance=request.user)
        profileUpdateForm = ProfileUpdateForm(request.POST, instance=profile)
        skillFormSet = SkillFormSet(request.POST, instance=profile, prefix='skills')
        experienceFormSet = ExperienceFormSet(request.POST, instance=profile, prefix='exp')
        roadmapFormSet = RoadmapFormSet(request.POST, instance=profile, prefix='road')

        if (
            userUpdateForm.is_valid()
            and profileUpdateForm.is_valid()
            and skillFormSet.is_valid()
            and experienceFormSet.is_valid()
            and roadmapFormSet.is_valid()
        ):
            userUpdateForm.save()
            profileUpdateForm.save()
            skillFormSet.save()
            experienceFormSet.save()
            roadmapFormSet.save()
            return redirect('resume_edit')
    else:
        userUpdateForm = UserUpdateForm(instance=request.user)
        profileUpdateForm = ProfileUpdateForm(instance=profile)
        skillFormSet = SkillFormSet(instance=profile, prefix='skills')
        experienceFormSet = ExperienceFormSet(instance=profile, prefix='exp')
        roadmapFormSet = RoadmapFormSet(instance=profile, prefix='road')

    context = {
        'userUpdateForm': userUpdateForm,
        'profileUpdateForm': profileUpdateForm,
        'skillFormSet': skillFormSet,
        'experienceFormSet': experienceFormSet,
        'roadmapFormSet': roadmapFormSet,
    }

    return render(request, 'resume_edit.html', context)


def resume(request, id):
    user = get_object_or_404(User, id=id) 
    context = {'user': user}
    return render(request, 'resume.html', context)


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








