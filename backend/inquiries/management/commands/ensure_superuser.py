"""
Create an initial admin user from environment variables (Railway / Docker).

Set in the backend service:
  DJANGO_SUPERUSER_EMAIL
  DJANGO_SUPERUSER_PASSWORD
Optional:
  DJANGO_SUPERUSER_USERNAME  (defaults to email)

Runs on every deploy but does nothing if a superuser already exists.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create superuser from DJANGO_SUPERUSER_* if no superuser exists."

    def handle(self, *args, **options):
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "").strip()
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip() or email

        if not email or not password:
            self.stdout.write(
                "DJANGO_SUPERUSER_EMAIL / DJANGO_SUPERUSER_PASSWORD not set; skipping."
            )
            return

        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("A superuser already exists; skipping.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(
                    f"User with username {username!r} already exists; skipping create."
                )
            )
            return

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )
        self.stdout.write(
            self.style.SUCCESS(f"Created superuser username={username!r} email={email!r}.")
        )
