import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from faker import Faker

from app_main.models import Profile, experience, Roadmap, Cinema, VideoGame


class Command(BaseCommand):
    help = 'Seeds database with 50 fake users at lightning speed using bulk operations'

    GAME_TITLES = [
        'The Witcher 3', 'Red Dead Redemption 2', 'Elden Ring', 'Cyberpunk 2077',
        'God of War', 'Dark Souls III', 'Portal 2', 'Hollow Knight', 'DOOM Eternal',
        'Half-Life: Alyx', 'Grand Theft Auto V', 'Skyrim', 'Apex Legends', 'Valorant',
        'BioShock Infinite', 'Mass Effect 2', 'Sekiro', 'Forza Horizon 5'
    ]

    CINEMA_TITLES = [
        'Breaking Bad', 'Interstellar', 'Inception', 'The Dark Knight',
        'Mr. Robot', 'Better Call Saul', 'Severance', 'The Matrix',
        'Blade Runner 2049', 'Stranger Things', 'Chernobyl', 'Succession',
        'Oppenheimer', 'Fight Club', 'Pulp Fiction', 'Whiplash'
    ]

    JOB_TITLES = [
        'Backend Developer', 'Frontend Engineer', 'Full-stack Developer',
        'DevOps Specialist', 'Machine Learning Engineer', 'Data Analyst',
        'System Administrator', 'Software Architect', 'QA Engineer', 'Mobile Developer'
    ]

    ROADMAP_MILESTONES = [
        'Learned Python & Data Structures',
        'Built full-stack Django projects',
        'Mastered Docker & CI/CD Pipelines',
        'Contributed to Open Source repositories',
        'Explored Deep Learning & PyTorch',
        'Designed Microservices Architecture',
        'Learned System Design & High Scalability'
    ]

    def handle(self, *args, **options):
        fake = Faker()
        total_users = 50

        self.stdout.write(self.style.NOTICE(f'Generating data for {total_users} users...'))

        education_keys = [c[0] for c in Profile.EDUCATION_CHOICES]
        field_keys = [c[0] for c in Profile.FIELD_CHOICES]
        media_type_keys = [c[0] for c in Cinema.MEDIA_TYPE_CHOICES]
        genre_keys = [c[0] for c in Cinema.GENRE_CHOICES]

        # 1. هش کردن پسورد فقط ۱ بار در کل برنامه به جای ۵۰ بار!
        hashed_password = make_password('GAPGPTMASKTOKEN3vdkp32iz89X0X')

        # لیست‌هایی برای نگه‌داری اشیاء قبل از ذخیره دسته‌جمعی
        users_to_create = []
        for _ in range(total_users):
            username = f"{fake.user_name()}_{random.randint(100, 9999)}"
            users_to_create.append(User(
                username=username,
                email=fake.unique.email(),
                password=hashed_password,
                first_name=fake.first_name(),
                last_name=fake.last_name()
            ))

        with transaction.atomic():
            # ایجاد ۵۰ یوزر در ۱ کوئری و دریافت IDهای ساخته شده
            created_users = User.objects.bulk_create(users_to_create)

            profiles = []
            experiences = []
            roadmaps = []
            cinemas = []
            games = []

            for user in created_users:
                # Profile
                profiles.append(Profile(
                    user=user,
                    phone=fake.phone_number(),
                    education=random.choice(education_keys),
                    description=random.choice(field_keys)
                ))

                # Experiences (1 to 3)
                for _ in range(random.randint(1, 3)):
                    experiences.append(experience(
                        user=user,
                        title=random.choice(self.JOB_TITLES),
                        details=fake.paragraph(nb_sentences=2)
                    ))

                # Roadmap (2 to 4)
                start_year = random.randint(2018, 2022)
                for idx in range(random.randint(2, 4)):
                    roadmaps.append(Roadmap(
                        user=user,
                        title=random.choice(self.ROADMAP_MILESTONES),
                        details=fake.sentence(nb_words=8),
                        year=str(start_year + idx)
                    ))

                # Cinema (2 to 4)
                for title in random.sample(self.CINEMA_TITLES, k=random.randint(2, 4)):
                    cinemas.append(Cinema(
                        user=user,
                        title=title,
                        media_type=random.choice(media_type_keys),
                        genre=random.choice(genre_keys),
                        reason=fake.sentence(nb_words=6)
                    ))

                # Video Games (2 to 4)
                for title in random.sample(self.GAME_TITLES, k=random.randint(2, 4)):
                    games.append(VideoGame(
                        user=user,
                        name=title,
                        level=random.randint(1, 5)
                    ))

            # اجرای کل اینسرت‌ها فقط با ۵ دستور SQL به جای صدها کوئری!
            Profile.objects.bulk_create(profiles)
            experience.objects.bulk_create(experiences)
            Roadmap.objects.bulk_create(roadmaps)
            Cinema.objects.bulk_create(cinemas)
            VideoGame.objects.bulk_create(games)

        self.stdout.write(self.style.SUCCESS(f'Done! Successfully created {total_users} users with bulk speed.'))
