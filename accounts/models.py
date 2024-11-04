from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone

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
    
class DailyCheckIn(models.Model):
    SKIN_FEEL_CHOICES = [
        ('dry', 'Dry'),
        ('oily', 'Oily'),
        ('normal', 'Normal'),
        ('itchy', 'Itchy'),
    ]
    
    HYDRATION_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
        ('not_sure', 'Not Sure'),
    ]
    
    SUN_EXPOSURE_CHOICES = [
        ('no', 'No'),
        ('some', 'Some'),
        ('a_lot', 'A lot'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    skin_feel = models.CharField(max_length=10, choices=SKIN_FEEL_CHOICES)
    new_blemishes = models.BooleanField()
    sleep_hours = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(24)]
    )
    hydration = models.CharField(max_length=10, choices=HYDRATION_CHOICES)
    sun_exposure = models.CharField(max_length=10, choices=SUN_EXPOSURE_CHOICES)
    stress_level = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    used_skincare = models.BooleanField()

    class Meta:
        unique_together = ['user', 'date']
        ordering = ['-date']

    def calculate_skin_feel_score(self):
        scores = {
            'dry': -1,
            'oily': -1,
            'normal': 1,
            'itchy': -2
        }
        return scores.get(self.skin_feel, 0)

    def calculate_sleep_score(self):
        if self.sleep_hours < 6:
            return -2
        elif self.sleep_hours < 7:
            return -1
        elif self.sleep_hours <= 8:
            return 0
        else:
            return 1

    def calculate_hydration_score(self):
        scores = {
            'yes': 1,
            'no': -1,
            'not_sure': 0
        }
        return scores.get(self.hydration, 0)

    def calculate_sun_exposure_score(self):
        scores = {
            'no': 0,
            'some': -1,
            'a_lot': -2
        }
        return scores.get(self.sun_exposure, 0)

    def calculate_stress_score(self):
        # Invert the stress level so higher stress = lower score
        return 6 - self.stress_level  # 5->1, 4->2, 3->3, 2->4, 1->5

    def calculate_skincare_score(self):
        return 1 if self.used_skincare else 0

    def calculate_composite_score(self):
        return sum([
            self.calculate_skin_feel_score(),
            -1 if self.new_blemishes else 0,  # -1 for yes, 0 for no
            self.calculate_sleep_score(),
            self.calculate_hydration_score(),
            self.calculate_sun_exposure_score(),
            self.calculate_stress_score(),
            self.calculate_skincare_score()
        ])