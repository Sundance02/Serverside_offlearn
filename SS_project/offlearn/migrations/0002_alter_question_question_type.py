# Generated by Django 5.1.1 on 2024-09-21 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offlearn', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='question_type',
            field=models.CharField(choices=[('Choice', 'Choice'), ('Text', 'Text')], max_length=10),
        ),
    ]