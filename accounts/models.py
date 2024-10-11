from django.contrib.auth.models import User
from django.db import models


class SkinType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)
    profile_picture = models.ImageField(default='default_pfp.jpg', upload_to='profile_pics/', null=True, blank=True)
    skin_type = models.ForeignKey(SkinType, on_delete=models.SET_NULL, null=True)
    skin_elasticity = models.CharField(max_length=50)
    skin_texture = models.CharField(max_length=50)
    acne_proneness = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.user.username}'s profile"