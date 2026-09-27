import random

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db import transaction
from faker import Faker

from app_main.models import Profile, experience, Roadmap, Cinema, VideoGame, Music


class Command(BaseCommand):
    help = "Cleans old data and seeds database with 50 fresh users"

    GAME_TITLES = [
        "The Witcher 3", "Red Dead Redemption 2", "Elden Ring", "Cyberpunk 2077",
        "God of War", "Dark Souls III", "Portal 2", "Hollow Knight", "DOOM Eternal",
        "Half-Life: Alyx", "Grand Theft Auto V", "Skyrim", "Apex Legends", "Valorant",
        "BioShock Infinite", "Mass Effect 2", "Sekiro", "Forza Horizon 5"
    ]

    CINEMA_TITLES = [
        "Breaking Bad", "Interstellar", "Inception", "The Dark Knight",
        "Mr. Robot", "Better Call Saul", "Severance", "The Matrix",
        "Blade Runner 2049", "Stranger Things", "Chernobyl", "Succession",
        "Oppenheimer", "Fight Club", "Pulp Fiction", "Whiplash"
    ]

    JOB_TITLES = [
        "Backend Developer", "Frontend Engineer", "Full-stack Developer",
        "DevOps Specialist", "Machine Learning Engineer", "Data Analyst",
        "System Administrator", "Software Architect", "QA Engineer", "Mobile Developer"
    ]

    ROADMAP_MILESTONES = [
        "Learned Python & Data Structures",
        "Built full-stack Django projects",
        "Mastered Docker & CI/CD Pipelines",
        "Contributed to Open Source repositories",
        "Explored Deep Learning & PyTorch",
        "Designed Microservices Architecture",
        "Learned System Design & High Scalability"
    ]

    SINGER_NAMES = [
        "Adele", "Eminem", "Ed Sheeran", "The Weeknd", "Billie Eilish",
        "Drake", "Taylor Swift", "Bruno Mars", "Coldplay", "Imagine Dragons",
        "Linkin Park", "Shawn Mendes", "Dua Lipa", "Sam Smith"
    ]

    def handle(self, *args, **options):
        fake = Faker()
        total_users = 50

        # ۱. پاک کردن کاربران قبلی بدون حذف اکانت ادمین
        self.stdout.write(self.style.WARNING("Deleting previous non-admin users and their data..."))
        deleted_count, _ = User.objects.filter(is_superuser=False).delete()
        self.stdout.write(self.style.SUCCESS(f"Deleted {deleted_count} old records."))

        # ۲. تولید دیتای جدید
        self.stdout.write(self.style.NOTICE(f"Generating data for {total_users} new users..."))

        education_keys = [choice[0] for choice in Profile.EDUCATION_CHOICES]
        field_keys = [choice[0] for choice in Profile.FIELD_CHOICES]
        media_type_keys = [choice[0] for choice in Cinema.MEDIA_TYPE_CHOICES]
        genre_keys = [choice[0] for choice in Cinema.GENRE_CHOICES]

        default_password = make_password("123")

        users_to_create = []
        for _ in range(total_users):
            username = f"{fake.user_name()}_{random.randint(100, 9999)}"
            users_to_create.append(
                User(
                    username=username,
                    email=fake.unique.email(),
                    password=default_password,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                )
            )

        with transaction.atomic():
            created_users = User.objects.bulk_create(users_to_create)

            profiles = []
            experiences = []
            roadmaps = []
            cinemas = []
            games = []
            musics = []

            for user in created_users:
                profiles.append(
                    Profile(
                        user=user,
                        phone=fake.phone_number(),
                        education=random.choice(education_keys),
                        description=random.choice(field_keys)
                    )
                )

                for _ in range(random.randint(1, 3)):
                    experiences.append(
                        experience(
                            user=user,
                            title=random.choice(self.JOB_TITLES),
                            details=fake.paragraph(nb_sentences=2)
                        )
                    )

                start_year = random.randint(2018, 2022)
                for idx in range(random.randint(2, 4)):
                    roadmaps.append(
                        Roadmap(
                            user=user,
                            title=random.choice(self.ROADMAP_MILESTONES),
                            details=fake.sentence(nb_words=8),
                            year=str(start_year + idx)
                        )
                    )

                for title in random.sample(self.CINEMA_TITLES, k=random.randint(2, 4)):
                    cinemas.append(
                        Cinema(
                            user=user,
                            title=title,
                            media_type=random.choice(media_type_keys),
                            genre=random.choice(genre_keys),
                            reason=fake.sentence(nb_words=6)
                        )
                    )

                for title in random.sample(self.GAME_TITLES, k=random.randint(2, 4)):
                    games.append(
                        VideoGame(
                            user=user,
                            name=title,
                            level=random.randint(1, 5)
                        )
                    )

                for _ in range(random.randint(1, 3)):
                    musics.append(
                        Music(
                            user=user,
                            singer_name=random.choice(self.SINGER_NAMES),
                            singer_description=fake.sentence(nb_words=10)
                        )
                    )

            Profile.objects.bulk_create(profiles)
            experience.objects.bulk_create(experiences)
            Roadmap.objects.bulk_create(roadmaps)
            Cinema.objects.bulk_create(cinemas)
            VideoGame.objects.bulk_create(games)
            Music.objects.bulk_create(musics)

        self.stdout.write(
            self.style.SUCCESS(f"Done! Successfully created {total_users} clean users with Music.")
        )
