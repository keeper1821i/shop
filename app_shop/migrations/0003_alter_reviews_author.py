# Generated by Django 4.1.3 on 2023-01-10 08:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_users', '0004_alter_profile_photo'),
        ('app_shop', '0002_alter_product_subcategory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reviews',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='author_article', to='app_users.profile'),
        ),
    ]
