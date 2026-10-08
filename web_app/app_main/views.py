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
    all_skills = [
        'Python', 'Django', 'FastAPI', 'REST API', 'PostgreSQL', 
        'Redis', 'Git', 'Docker', 'Linux', 'JavaScript', 
        'TypeScript', 'React', 'HTML/CSS', 'SQL'
    ]
    all_majors = [
        ('software_eng', 'Software Engineering'),
        ('ai_ml', 'Artificial Intelligence & Machine Learning'),
        ('data_science', 'Data Science & Big Data'),
        ('cybersecurity', 'Cybersecurity & Network Defense'),
        ('web_dev', 'Web Development'),
        ('devops', 'DevOps & Cloud Computing'),
        ('hardware_embedded', 'Hardware & Embedded Systems'),
        ('game_dev', 'Game Development'),
        ('other', 'Other')
    ]
    all_degrees = [
        ('associate', 'Associate Degree'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('doctorate', 'Doctorate / Ph.D.'),
        ('other', 'Other'),
    ]
    q = request.GET.get('q', '')
    skills = request.GET.getlist('skill')
    degree = request.GET.get('degree', '')
    major = request.GET.get('major', '')
    users = User.objects.all()

    if q:
        users = users.filter(
            Q(first_name__icontains=q) |
            Q(last_name__icontains=q) |
            Q(profile__skills__name__icontains=q)
        )

    if skills:
        for s in skills:
            users = users.filter(profile__skills__name=s)

    if degree:
        users = users.filter(profile__education=degree)

    if major:
        users = users.filter(profile__description=major)

    users = users.distinct().order_by('id')

    items_per_page = 9
    paginator = Paginator(users, items_per_page)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'q': q,
        'skills': skills,
        'degree': degree,
        'major': major,
        'all_skills': all_skills,
        'all_majors': all_majors,
        'all_degrees': all_degrees
    }

    return render(request, "index.html", context)








