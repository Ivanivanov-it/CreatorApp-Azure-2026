from django.conf import settings
from django.db import models
from django.utils.text import slugify

from common.choices import CharacterType
from common.models import TimeStampModel, CombatStatModel, Role


class Enemy(TimeStampModel,CombatStatModel):

    name = models.CharField(max_length=100,unique=True)
    title = models.CharField(max_length=100,unique=True)
    type = models.CharField(choices=CharacterType.choices,default=CharacterType.OTHER)
    weakness = models.ManyToManyField(Role, related_name='enemies')
    description = models.TextField()
    slug = models.SlugField(max_length=100,unique=True,blank=True)
    image_url = models.URLField(blank=True,null=True)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='enemies')


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.title}")

        # if not self.image_url:
        #     self.image_url = f"{settings.STATIC_URL}images/enemy.png"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name