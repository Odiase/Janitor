# Generated by Django 5.0.6 on 2024-06-11 20:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='artisanprofile',
            name='profile_image',
            field=models.ImageField(upload_to='user_uploads/artisans/artisans_profile_images'),
        ),
    ]
