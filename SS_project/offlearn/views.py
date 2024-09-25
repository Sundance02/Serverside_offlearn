from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from employee.forms import *
from django.views import View
from django.db import transaction
from offlearn.models import *   
from .forms import *
from django.forms import modelformset_factory


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

class student_quiz_answer(View):
    def get(self, request):
        return render(request, 'student_quiz_answer.html')

class student_quiz_detail(View):
    def get(self, request):
        return render(request, 'student_quiz_detail.html')
    

class create_quiz(View):

    def get(self, request, course_id):
        quizform = AddQuizForm()
        course = Course.objects.get(pk=course_id)
        return render(request, 'Create_Quiz.html', {"form": quizform, 'course': course})
    
    def post(self, request, course_id):
        form = AddQuizForm(request.POST)
        course = Course.objects.get(pk=course_id)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.course = course
            quiz.save()

            return redirect('question_list', quiz.id)
        
        return render(request, 'Create_Quiz.html', {'form': form, 'course': course})


class add_choice_question(View):

    def get(self, request, quiz_id):
        
        ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=2)
        formset = ChoiceFormSet(queryset=Choice.objects.none())
        quiz = Quiz.objects.get(pk=quiz_id)
        return render(request, 'choice_question.html', {'choiceform': formset, 'questionform': AddQuestionForm(), 'quiz': quiz})
    
    def post(self, request, quiz_id):

        questionform = AddQuestionForm(request.POST)
        quiz = Quiz.objects.get(pk=quiz_id)
        ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=10)
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if questionform.is_valid() and formset.is_valid():
            quest = questionform.save(commit=False)
            quest.quiz = quiz
            quest.save()

            for form in formset:

                choice = form.save(commit=False)
                choice.question = quest
                choice.save()

            return redirect('question_list', quiz_id)
        
        print(formset.errors)
        return render(request, 'choice_question.html', {'questionform': questionform, 'choiceform': formset, 'quiz': quiz})



class add_context_question(View):

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        form = AddQuestionForm()
        return render(request, 'context_question.html', {'questionform': form, 'quiz': quiz})
    
    def post(self, request, quiz_id):

        form = AddQuestionForm(request.POST)
        quiz = Quiz.objects.get(pk=quiz_id)

        if form.is_valid():
            quest = form.save(commit=False)
            quest.quiz = Quiz.objects.get(pk=quiz_id)
            quest.save()
            return redirect('question_list', quiz_id)
        print(form.errors)
        return render(request, 'context_question.html', {'questionform': form, 'quiz': quiz})


class question_list(View):

    def get(self, request, quiz_id):
        quizer = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.filter(quiz = quizer)
        return render(request, 'Question_list.html', {'quiz': quizer, 'question': question})
