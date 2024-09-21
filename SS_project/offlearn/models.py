from django.db import models

# Create your models here.
from django.db import models

# User model
class User(models.Model):
    user_name = models.CharField(max_length=20, unique=True, null=False)
    password = models.CharField(max_length=20, null=False)

    def __str__(self):
        return self.user_name


# Student model
class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    courses = models.ManyToManyField('Course', related_name='students')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Instructor model
class Instructor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    courses = models.ManyToManyField('Course', related_name='instructors')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Course model
class Course(models.Model):
    course_name = models.CharField(max_length=80, null=False)
    course_description = models.CharField(max_length=255)
    course_image = models.CharField(max_length=255)

    def __str__(self):
        return self.course_name


# Content model
class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=80)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.content_name


# Material model
class Material(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file_path


# Quiz model
class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255, null=False)
    deadline = models.DateTimeField(null=False)
    max_point = models.IntegerField(null=False)

    def __str__(self):
        return self.quiz_name


# Question model
class Question(models.Model):
    class QuestionType(models.Choices):
        Choice = "Choice"
        Text = "Text"
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=255, null=False)
    point = models.IntegerField(null=False)
    question_type = models.CharField(max_length=10, choices=QuestionType.choices)  # Enum: single/multiple choice, etc.

    def __str__(self):
        return self.question_name


# Choice model
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_name = models.CharField(max_length=80)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_name


# StudentAnswer model
class StudentAnswer(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=255)
    submit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_answer


# QuizScore model
class QuizScore(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"Score: {self.score} for {self.quiz.quiz_name}"
