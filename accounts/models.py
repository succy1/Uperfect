from django.contrib.auth.models import User
from django.db import models

class SkinType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SkinCondition(models.Model):
    condition_type = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.condition_type

class SkincareGoal(models.Model):
    goal = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.goal

class SubscriptionTier(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.BigIntegerField()

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skin_types = models.ManyToManyField(SkinType)
    skin_conditions = models.ManyToManyField(SkinCondition)
    skincare_goals = models.ManyToManyField(SkincareGoal)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, null=True, blank=True)
    special_health_conditions = models.TextField(null=True, blank=True)
    sun_exposure_level = models.CharField(max_length=20, null=True, blank=True)
    pollution_exposure_level = models.CharField(max_length=20, null=True, blank=True)
    physical_activity_level = models.CharField(max_length=20, null=True, blank=True)
    profile_picture = models.ImageField(default='profile_pics/default_pfp.png', upload_to='profile_pics/', null=True, blank=True)
    subscription_tier = models.ForeignKey(SubscriptionTier, on_delete=models.SET_NULL, null=True, blank=True)


    def __str__(self):
        return f"{self.user.username}'s profile"
    
class SkincareAdvice(models.Model):
    skin_type = models.ForeignKey(SkinType, on_delete=models.CASCADE, related_name="advices")
    content = models.CharField(max_length=1000)

    def __str__(self):
        return f"{self.skin_type.name} - {self.content}"