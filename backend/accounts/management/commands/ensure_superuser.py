import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = (
        "Create the initial superuser from DJANGO_SUPERUSER_EMAIL and "
        "DJANGO_SUPERUSER_PASSWORD, but only if no superuser exists yet. "
        "Existing accounts are never modified, so it is safe to run on every start."
    )

    def handle(self, *args, **options):
        User = get_user_model()
        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write("Superuser already exists; nothing to do.")
            return

        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if not email or not password:
            self.stdout.write(self.style.WARNING(
                "No superuser exists. Set DJANGO_SUPERUSER_EMAIL and "
                "DJANGO_SUPERUSER_PASSWORD to create one, or run "
                "`manage.py createsuperuser`."
            ))
            return

        try:
            validate_password(password)
        except ValidationError as error:
            raise CommandError("DJANGO_SUPERUSER_PASSWORD rejected: " + " ".join(error.messages))

        User.objects.create_superuser(email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"Created superuser {email}."))
