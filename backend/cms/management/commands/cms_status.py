"""Print database path, staff users, and CMS row counts (debug empty admin)."""

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cms.models import (
    AboutSettings,
    BlogPost,
    HeroSettings,
    HomePillar,
    HomeShowcase,
    HomeStat,
    HomeTestimonial,
    Project,
    Service,
    SocialLink,
)


class Command(BaseCommand):
    help = "Show SQLite path, staff user count, and CMS table row counts."

    def handle(self, *args, **options):
        db = settings.DATABASES["default"]
        name = db.get("NAME", "")
        self.stdout.write(self.style.NOTICE(f"Database engine: {db.get('ENGINE')}"))
        self.stdout.write(f"Database file: {name}")

        User = get_user_model()
        total_users = User.objects.count()
        staff = User.objects.filter(is_staff=True).count()
        superusers = User.objects.filter(is_superuser=True).count()
        self.stdout.write(
            f"Users: {total_users} total, {staff} staff (can open /admin/), "
            f"{superusers} superuser(s)."
        )
        if staff == 0:
            self.stdout.write(
                self.style.ERROR(
                    "No staff users — run: python manage.py createsuperuser"
                )
            )

        self.stdout.write("")
        self.stdout.write("CMS row counts:")
        models = [
            ("Home - Hero", HeroSettings),
            ("About page", AboutSettings),
            ("Home - Pillar cards", HomePillar),
            ("Home - Showcase blocks", HomeShowcase),
            ("Home - Stats", HomeStat),
            ("Home - Testimonials", HomeTestimonial),
            ("Services", Service),
            ("Blog posts", BlogPost),
            ("Social links", SocialLink),
            ("Projects", Project),
        ]
        # Projects often stay empty until you upload cover images in admin.
        warn_if_empty = [m for m in models if m[1] is not Project]
        needs_seed = all(Model.objects.count() == 0 for _, Model in warn_if_empty)

        for label, Model in models:
            self.stdout.write(f"  {label}: {Model.objects.count()}")

        self.stdout.write("")
        if needs_seed:
            self.stdout.write(
                self.style.WARNING(
                    "CMS looks empty. Run: python manage.py migrate && python manage.py seed_cms"
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    "CMS has data. Open /admin/ and expand the **CMS** section."
                )
            )

        self.stdout.write(
            "\nAdmin URL: /admin/ - expand **CMS** and **Inquiries** on the index page."
        )
