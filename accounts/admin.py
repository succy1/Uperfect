from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(SkinType)
admin.site.register(Profile)
admin.site.register(SkinCondition)
admin.site.register(SkincareGoal)
admin.site.register(SubscriptionTier)
admin.site.register(SkincareAdvice)
admin.site.register(DailyCheckIn)