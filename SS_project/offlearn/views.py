from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.db import transaction
from offlearn.models import *
from .forms import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from offlearn.forms import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import login, logout



class show_course(View):
    def get(self, request):
        if(request.user.groups.filter(name="Student").exists()):
            print(request.user.id)
            user_course = Course.objects.filter(user_course__id = request.user.id)
            context = {"courses":user_course}
            page = "Allcourse-Student.html"
        elif(request.user.groups.filter(name="Instructor").exists()):
            user_course = Course.objects.filter(user_course__id = request.user.id)
            context = {"courses":user_course}
            page = "Allcourse-Teacher.html"
        else:
            user_course = Course.objects.all()
            context = {"courses":user_course}
            page = "Allcourse-Guest.html"
        return render(request, page, context)  
        
  
    
class create_course(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Create_Course.html')

class edit_course(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Edit_Course.html')

class create_topic(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Create_Topic.html')

class edit_topic(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Edit_Topic.html')

class profile(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Profile.html')
    
class view_description(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'view_description.html')
    



class Register(View):
    def get(self, request):
        print('yahaloooo')
        form = Registerform()
        return render(request, 'Register.html', {"form": form})
    
    def post(self, request):
        form = Registerform(request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Student')
            user.groups.add(group)
            user.save
            messages.success(request, 'Account created successfully')  
            return redirect('Login')
        return render(request, 'Register.html', {"form": form})


class Login(View):
    def get(self, request):
        form = Loginform()
        return render(request, 'Login.html', {"form": form})

    def post(self, request):
        form = Loginform(data = request.POST)
        if form.is_valid(): 
            user = form.get_user()
            login(request, user)
            return redirect('show_course')
        return render(request, 'Login.html', {"form": form})

class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('Login')
    



class Course_Detail_student(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'show_selected_course_student.html')
    
class Course_Detail_teacher(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'show_selected_course_teacher.html')

class Student_List(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'student_list.html')
    

class teacher_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'teacher_quiz.html')
    
class teacher_quiz_detail(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'teacher_quiz_detail.html')
    
class student_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'student_quiz.html')

class student_quiz_answer(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'student_quiz_answer.html')

class student_quiz_detail(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'student_quiz_detail.html')

class create_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        quizform = AddQuizForm()
        return render(request, 'create_quiz.html', {"form": quizform})


class add_choice_question(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'partials/choice_question.html', {'choiceform': AddChoiceForm(), 'questionform': AddQuestionForm()})
    
    def post(self, request):
        pass


class add_choice(LoginRequiredMixin, View):
    login_url = '/Login/'

    def get(self, request):
        return render(request, 'partials/addchoice.html', {'choiceform': AddChoiceForm()})
    
    def post(self, request):
        pass


class add_context_question(LoginRequiredMixin, View):
    login_url = '/Login/'

    def get(self, request):
        return render(request, 'partials/context_question.html', {'questionform': AddQuestionForm()})
    
    def post(self, request):
        pass