from django.shortcuts import render
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from employee.forms import *
from django.views import View
from django.db import transaction
from offlearn.models import *



class show_course_guest(View):
    def get(self, request):
        return render(request, 'Allcourse-Guest.html')

class show_course_student(View):
    def get(self, request):
        return render(request, 'Allcourse-Student.html')
    
class show_course_teacher(View):
    def get(self, request):
        return render(request, 'Allcourse-Teacher.html')    
    
class create_course(View):
    def get(self, request):
        return render(request, 'Create_Course.html')

class edit_course(View):
    def get(self, request):
        return render(request, 'Edit_Course.html')

class create_topic(View):
    def get(self, request):
        return render(request, 'Create_Topic.html')

class edit_topic(View):
    def get(self, request):
        return render(request, 'Edit_Topic.html')

class profile(View):
    def get(self, request):
        return render(request, 'Profile.html')
    
class view_description(View):
    def get(self, request):
        return render(request, 'view_description.html')
    
class Register(View):
    def get(self, request):
        return render(request, 'Register.html')

class Login(View):
    def get(self, request):
        return render(request, 'Login.html')
    
class Course_Detail_student(View):
    def get(self, request):
        return render(request, 'show_selected_course_student.html')
    
class Course_Detail_teacher(View):
    def get(self, request):
        return render(request, 'show_selected_course_teacher.html')

class Student_List(View):
    def get(self, request):
        return render(request, 'student_list.html')
    

class teacher_quiz(View):
    def get(self, request):
        return render(request, 'teacher_quiz.html')
    
class teacher_quiz_detail(View):
    def get(self, request):
        return render(request, 'teacher_quiz_detail.html')
    
class student_quiz(View):
    def get(self, request):
        return render(request, 'student_quiz.html')
