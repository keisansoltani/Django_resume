import random
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import transaction
from faker import Faker

from app_main.models import Profile, experience, Roadmap, Cinema, VideoGame, Music, Skill


class Command(BaseCommand):
    help = "Seed database with realistic resumes for directory testing"

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

    SKILL_NAMES = [
        "Python", "Django", "FastAPI", "REST API", "PostgreSQL", "Redis",
        "Git", "Docker", "Linux", "JavaScript", "TypeScript", "React",
        "HTML/CSS", "SQL"
    ]

    def handle(self, *args, **options):
        fake = Faker()

        users = list(User.objects.filter(is_superuser=False).order_by("id"))
        if not users:
            self.stdout.write(self.style.ERROR("No users found. Please create some users first."))
            return

        education_keys = [c[0] for c in Profile.EDUCATION_CHOICES]
        field_keys = [c[0] for c in Profile.FIELD_CHOICES]
        media_type_keys = [c[0] for c in Cinema.MEDIA_TYPE_CHOICES]
        genre_keys = [c[0] for c in Cinema.GENRE_CHOICES]

        with transaction.atomic():
            experience.objects.filter(user__in=users).delete()
            Roadmap.objects.filter(user__in=users).delete()
            Cinema.objects.filter(user__in=users).delete()
            VideoGame.objects.filter(user__in=users).delete()
            Music.objects.filter(user__in=users).delete()
            Skill.objects.filter(user__in=users).delete()

            existing_profiles = {p.user_id: p for p in Profile.objects.filter(user__in=users)}
            profiles_to_create = []
            profiles_to_update = []

            for u in users:
                prof = existing_profiles.get(u.id)
                if prof:
                    prof.phone = fake.phone_number()
                    prof.education = random.choice(education_keys)
                    prof.description = random.choice(field_keys)
                    profiles_to_update.append(prof)
                else:
                    profiles_to_create.append(
                        Profile(
                            user=u,
                            phone=fake.phone_number(),
                            education=random.choice(education_keys),
                            description=random.choice(field_keys)
                        )
                    )

            if profiles_to_create:
                Profile.objects.bulk_create(profiles_to_create)
            if profiles_to_update:
                Profile.objects.bulk_update(profiles_to_update, ["phone", "education", "description"])

            experiences = []
            roadmaps = []
            cinemas = []
            games = []
            musics = []
            skills = []

            for u in users:
                for _ in range(random.randint(1, 3)):
                    experiences.append(
                        experience(
                            user=u,
                            title=random.choice(self.JOB_TITLES),
                            details=fake.paragraph(nb_sentences=2)
                        )
                    )

                start_yr = random.randint(2018, 2022)
                for i in range(random.randint(2, 4)):
                    roadmaps.append(
                        Roadmap(
                            user=u,
                            title=random.choice(self.ROADMAP_MILESTONES),
                            details=fake.sentence(nb_words=8),
                            year=str(start_yr + i)
                        )
                    )

                for title in random.sample(self.CINEMA_TITLES, k=random.randint(2, 4)):
                    cinemas.append(
                        Cinema(
                            user=u,
                            title=title,
                            media_type=random.choice(media_type_keys),
                            genre=random.choice(genre_keys),
                            reason=fake.sentence(nb_words=6)
                        )
                    )

                for title in random.sample(self.GAME_TITLES, k=random.randint(2, 4)):
                    games.append(
                        VideoGame(
                            user=u,
                            name=title,
                            level=random.randint(1, 5)
                        )
                    )

                for _ in range(random.randint(1, 3)):
                    musics.append(
                        Music(
                            user=u,
                            singer_name=random.choice(self.SINGER_NAMES),
                            singer_description=fake.sentence(nb_words=10)
                        )
                    )

                for name in random.sample(self.SKILL_NAMES, k=random.randint(4, 7)):
                    skills.append(
                        Skill(
                            user=u,
                            name=name,
                            level=random.randint(1, 5)
                        )
                    )

            experience.objects.bulk_create(experiences)
            Roadmap.objects.bulk_create(roadmaps)
            Cinema.objects.bulk_create(cinemas)
            VideoGame.objects.bulk_create(games)
            Music.objects.bulk_create(musics)
            Skill.objects.bulk_create(skills)

        self.stdout.write(self.style.SUCCESS(f"Successfully seeded/updated {len(users)} users with new resume data."))


