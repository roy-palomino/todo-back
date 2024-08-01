from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from ...models import UserSettings


class Command(BaseCommand):
    help = 'Create UserSettings for users without them'

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users_without_settings = User.objects.filter(settings__isnull=True)
        for user in users_without_settings:
            UserSettings.objects.create(user=user)
            self.stdout.write(self.style.SUCCESS(f'Settings created for user {user.username}'))
