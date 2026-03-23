from cloudinary.models import CloudinaryField
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.




class CustomUser(AbstractUser):
    picture = CloudinaryField('image')



class UserBattleStats(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,primary_key=True,related_name='stats')
    wins = models.IntegerField(default=0)
    losses = models.IntegerField(default=0)

    def add_win(self):
        self.wins += 1
        self.save(update_fields=['wins'])

    def add_loss(self):
        self.losses += 1
        self.save(update_fields=['losses'])

    def get_user_winrate(self):
        total = self.wins + self.losses
        if total == 0:
            return 0

        return round((self.wins / total)  * 100, 2)

    def __str__(self):
        return self.user.username