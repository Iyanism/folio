import re
import secrets

from django.db.models.signals import post_save
from django.dispatch.dispatcher import receiver
from django.db import IntegrityError

from accounts.models import User, UserProfile

def _generate_username(email):
    email = email.split("@")[0].lower()[:5]
    secret_code = secrets.token_hex(3)
    return f"{re.sub('[^a-z0-9]', '', email)}{secret_code}"

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            UserProfile.objects.create(user=instance, username=_generate_username(instance.email))
            return
        except IntegrityError:
            raise RuntimeError(f"Could not generate unique username for user {instance.pk}")

