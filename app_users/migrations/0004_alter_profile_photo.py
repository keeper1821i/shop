# Generated by Django 4.1.3 on 2023-01-06 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0003_alter_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='photo',
            field=models.ImageField(default='photo/no_photo.jpg', upload_to='photo/'),
        ),
    ]