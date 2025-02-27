# Generated by Django 5.1.1 on 2024-10-26 19:43

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_rename_skin_types_skincareadvice_skin_type'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='skincareadvice',
            name='skin_type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='advices', to='accounts.skintype'),
        ),
        migrations.CreateModel(
            name='DailyCheckIn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now_add=True)),
                ('skin_feel', models.CharField(choices=[('dry', 'Dry'), ('oily', 'Oily'), ('normal', 'Normal'), ('itchy', 'Itchy')], max_length=10)),
                ('new_blemishes', models.BooleanField()),
                ('sleep_hours', models.DecimalField(decimal_places=1, max_digits=3, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(24)])),
                ('hydration', models.CharField(choices=[('yes', 'Yes'), ('no', 'No'), ('not_sure', 'Not Sure')], max_length=10)),
                ('sun_exposure', models.CharField(choices=[('no', 'No'), ('some', 'Some'), ('a_lot', 'A lot')], max_length=10)),
                ('stress_level', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('used_skincare', models.BooleanField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-date'],
                'unique_together': {('user', 'date')},
            },
        ),
    ]
