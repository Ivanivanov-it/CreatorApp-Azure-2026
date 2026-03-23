from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from accounts.models import UserBattleStats

UserModel = get_user_model()

@receiver(post_save,sender=UserModel)
def create_user_battle_stats(sender, instance, created, **kwargs):
    if created:
        UserBattleStats.objects.create(user=instance)

@receiver(pre_save,sender=UserModel)
def log_username_change(sender, instance, **kwargs):

    """
    I should create log model or smth later and save the signals there instead
    """

    if not instance.pk:
        return

    try:
        old_data = UserModel.objects.get(pk=instance.pk)
        if old_data.username != instance.username:
            print(f"Username changed from {old_data.username} to {instance.username}")
    except UserModel.DoesNotExist:
        pass
