# Generated by Django 5.1.1 on 2024-09-21 13:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=80)),
                ('course_description', models.CharField(max_length=255)),
                ('course_image', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_name', models.CharField(max_length=255)),
                ('point', models.IntegerField()),
                ('question_type', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=20, unique=True)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content_name', models.CharField(max_length=80)),
                ('description', models.CharField(blank=True, max_length=255, null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.course')),
            ],
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_path', models.CharField(max_length=255)),
                ('video_url', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.content')),
            ],
        ),
        migrations.CreateModel(
            name='Choice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('choice_name', models.CharField(max_length=80)),
                ('is_correct', models.BooleanField(default=False)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.question')),
            ],
        ),
        migrations.CreateModel(
            name='Quiz',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quiz_name', models.CharField(max_length=255)),
                ('deadline', models.DateTimeField()),
                ('max_point', models.IntegerField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.course')),
            ],
        ),
        migrations.AddField(
            model_name='question',
            name='quiz',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.quiz'),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(related_name='students', to='offlearn.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='offlearn.user')),
            ],
        ),
        migrations.CreateModel(
            name='QuizScore',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField()),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.quiz')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.student')),
            ],
        ),
        migrations.CreateModel(
            name='StudentAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_answer', models.CharField(max_length=255)),
                ('submit_date', models.DateTimeField(auto_now_add=True)),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.choice')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.question')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offlearn.student')),
            ],
        ),
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('courses', models.ManyToManyField(related_name='instructors', to='offlearn.course')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='offlearn.user')),
            ],
        ),
    ]
