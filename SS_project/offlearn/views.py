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


class show_course_guest(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Allcourse-Guest.html')

class show_course_student(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Allcourse-Student.html')
    
class show_course_teacher(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Allcourse-Teacher.html')    
    
class create_course(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Create_Course.html')

class edit_course(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Edit_Course.html')

class create_topic(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Create_Topic.html')

class edit_topic(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Edit_Topic.html')

class profile(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'Profile.html')
    
class view_description(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'view_description.html')
    



class Register(View):
    def get(self, request):
        form = Registerform()
        return render(request, 'Register.html', {"form": form})
    
    def post(self, request):
        form = Registerform(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully')  
            return redirect('Login')
        return render(request, 'Register.html', {"form": form})


class Login(View):
    def get(self, request):
        return render(request, 'Login.html')
    



class Course_Detail_student(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'show_selected_course_student.html')
    
class Course_Detail_teacher(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'show_selected_course_teacher.html')

class Student_List(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'student_list.html')
    

class teacher_quiz(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'teacher_quiz.html')
    
class teacher_quiz_detail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'teacher_quiz_detail.html')
    
class student_quiz(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'student_quiz.html')

class student_quiz_answer(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'student_quiz_answer.html')

class student_quiz_detail(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'student_quiz_detail.html')

class create_quiz(LoginRequiredMixin, View):
    def get(self, request):
        quizform = AddQuizForm()
        return render(request, 'create_quiz.html', {"form": quizform})


class add_choice_question(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'partials/choice_question.html', {'choiceform': AddChoiceForm(), 'questionform': AddQuestionForm()})
    
    def post(self, request):
        pass


class add_choice(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'partials/addchoice.html', {'choiceform': AddChoiceForm()})
    
    def post(self, request):
        pass


class add_context_question(LoginRequiredMixin, View):

    def get(self, request):
        return render(request, 'partials/context_question.html', {'questionform': AddQuestionForm()})
    
    def post(self, request):
        pass