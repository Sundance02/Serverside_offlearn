# Generated by Django 5.1.1 on 2024-09-25 10:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offlearn', '0005_alter_user_info_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_info',
            name='profile_image',
            field=models.ImageField(upload_to='profile/'),
        ),
    ]
