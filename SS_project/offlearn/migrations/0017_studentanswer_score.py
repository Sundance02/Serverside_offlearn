# Generated by Django 5.1.1 on 2024-09-29 08:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('offlearn', '0016_studentanswer_quiz'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentanswer',
            name='score',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='offlearn.quizscore'),
        ),
    ]