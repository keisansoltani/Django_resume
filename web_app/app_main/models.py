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


class Cinema(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('series', 'Series'),
        ('film', 'Film'),
        ('tv', 'TV'),
        ('other', 'Other'),
    ]

    GENRE_CHOICES = [
        ('action', 'Action'),
        ('comedy', 'Comedy'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('romance', 'Romance'),
        ('scifi', 'Sci-Fi'),
        ('thriller', 'Thriller'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cinemas')
    title = models.CharField(max_length=100)  # عنوان فیلم یا سریال (مثلاً Breaking Bad)
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPE_CHOICES)  # نوع (فیلم، سریال، ...)
    genre = models.CharField(max_length=30, choices=GENRE_CHOICES)  # ژانر
    reason = models.TextField(blank=True)  # چرا این رو پیشنهاد یا دوست داری؟



class VideoGame(models.Model):
    LEVEL_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='games')
    name=models.CharField(max_length=100,null=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)


class Music(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True,related_name='music')
    singer_name=models.CharField(max_length=100)
    singer_description=models.TextField(blank=True, default="")

    def __str__(self):
        return f"{self.singer_name} | {self.singer_description}" if self.singer_description else self.singer_name



class Skill(models.Model):
    LEVEL_CHOICES = [
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='skills')
    name = models.CharField(max_length=100, null=True)
    level = models.PositiveSmallIntegerField(choices=LEVEL_CHOICES, default=1)
    