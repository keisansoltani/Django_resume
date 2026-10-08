from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth.models import User
from .models import Profile, experience, Roadmap, Skill

SKILL_CHOICES = [
    ('', '---------'),
    ('Python', 'Python'),
    ('Django', 'Django'),
    ('FastAPI', 'FastAPI'),
    ('REST API', 'REST API'),
    ('PostgreSQL', 'PostgreSQL'),
    ('Redis', 'Redis'),
    ('Git', 'Git'),
    ('Docker', 'Docker'),
    ('Linux', 'Linux'),
    ('JavaScript', 'JavaScript'),
    ('TypeScript', 'TypeScript'),
    ('React', 'React'),
    ('HTML/CSS', 'HTML/CSS'),
    ('SQL', 'SQL'),
]

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'education', 'description']

class ExperienceForm(forms.ModelForm):
    class Meta:
        model = experience
        fields = ['title', 'details']

class RoadmapForm(forms.ModelForm):
    class Meta:
        model = Roadmap
        fields = ['title', 'details', 'year']

class SkillForm(forms.ModelForm):
    name = forms.ChoiceField(choices=SKILL_CHOICES)

    class Meta:
        model = Skill
        fields = ['name', 'level']

SkillFormSet = inlineformset_factory(
    Profile,
    Skill,
    form=SkillForm,
    extra=1,
    can_delete=True,
)

ExperienceFormSet = inlineformset_factory(
    Profile,
    experience,
    form=ExperienceForm,
    extra=1,
    can_delete=True,
)

RoadmapFormSet = inlineformset_factory(
    Profile,
    Roadmap,
    form=RoadmapForm,
    extra=1,
    can_delete=True,
)

