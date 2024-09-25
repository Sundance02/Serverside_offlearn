from django.db import models
# Create your models here.
from django.db import models
from django.contrib.auth.models import User




class User_Info(models.Model):
    class Role(models.Choices):
        Choice = "Student"
        Text = "Instructor"
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=Role.choices)
    profile_image = models.ImageField()



class Course(models.Model):
    user_course = models.ManyToManyField(User)
    course_name = models.CharField(max_length=80, null=False)
    course_description = models.CharField(max_length=255)
    course_image = models.ImageField()
    # เพิ่มอาจารย์ผู้สอน
    def __str__(self):
        return self.course_name



class Content(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    content_name = models.CharField(max_length=80)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.content_name



class Material(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    file_path = models.CharField(max_length=255)
    video_url = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.file_path



class Quiz(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    quiz_name = models.CharField(max_length=255, null=False)
    deadline = models.DateTimeField(null=False)
    max_point = models.IntegerField(null=False)

    def __str__(self):
        return self.quiz_name



class Question(models.Model):
    class QuestionType(models.Choices):
        Choice = "Choice"
        Text = "Text"
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    question_name = models.CharField(max_length=255, null=False)
    point = models.IntegerField(null=False)
    question_type = models.CharField(max_length=10, choices=QuestionType.choices)

    def __str__(self):
        return self.question_name



class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_name = models.CharField(max_length=80)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_name



class StudentAnswer(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    text_answer = models.CharField(max_length=255, null=True)
    text_answer = models.CharField(max_length=255, null=True)
    submit_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text_answer



class QuizScore(models.Model):
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    score = models.IntegerField()

    def __str__(self):
        return f"Score: {self.score} for {self.quiz.quiz_name}"