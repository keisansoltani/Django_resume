from django.db import models
from django.contrib.auth.models import User



class Profile(models.Model):
    EDUCATION_CHOICES = [
        ('associate', 'Associate Degree'),
        ('bachelor', "Bachelor's Degree"),
        ('master', "Master's Degree"),
        ('doctorate', 'Doctorate / Ph.D.'),
        ('other', 'Other'),
    ]
    FIELD_CHOICES = [
        ('software_eng', 'Software Engineering'),
        ('ai_ml', 'Artificial Intelligence & Machine Learning'),
        ('data_science', 'Data Science & Big Data'),
        ('cybersecurity', 'Cybersecurity & Network Defense'),
        ('web_dev', 'Web Development'),
        ('devops', 'DevOps & Cloud Computing'),
        ('hardware_embedded', 'Hardware & Embedded Systems'),
        ('game_dev', 'Game Development'),
        ('other', 'Other'),
    ]
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    phone=models.CharField(max_length=50)
    education=models.CharField(max_length=50,null=True,choices=EDUCATION_CHOICES)
    description=models.TextField(null=True,choices=FIELD_CHOICES)
    
    @property
    def get_education(self):
        return dict(self.EDUCATION_CHOICES).get(self.education)



class experience(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70)
    details=models.TextField()
    



class Roadmap(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title=models.CharField(max_length=70,null=True)
    details=models.TextField(null=True)
    year=models.CharField(max_length=4)

