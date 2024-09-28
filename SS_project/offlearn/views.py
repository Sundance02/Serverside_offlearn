from django.shortcuts import render, redirect
from django.db.models import *
from django.db.models.functions import *
from django.db.models.lookups import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.db import transaction
from offlearn.models import *   
from .forms import *
from django.forms import modelformset_factory
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.models import Group

class show_course(View):
    def get(self, request):
        if(request.user.groups.filter(name="Student").exists()):
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
        
class searched_course(View):
    def post(self, request):
        if(request.user.groups.filter(name="Student").exists()):
            page = "Allcourse-Student.html"
        elif(request.user.groups.filter(name="Instructor").exists()):
            page = "Allcourse-Teacher.html"
        else:
            page = "Allcourse-Guest.html"
      
        searched_info = request.POST['searched']
        result = Course.objects.filter(course_name__icontains = searched_info)
        context = {"courses":result}
        return render(request, page, context)
    def get(self, request):
        if(request.user.groups.filter(name="Student").exists()):
            page = "Allcourse-Student.html"
        elif(request.user.groups.filter(name="Instructor").exists()):
            page = "Allcourse-Teacher.html"
        else:
            page = "Allcourse-Guest.html"
        result = ""       
        filter = request.GET.get('filter')
        if(filter == "all"):
            result = Course.objects.all()
        elif(filter == "own"):
            result = Course.objects.filter(user_course__id = request.user.id)
        elif(filter == "notown"):
            result = Course.objects.exclude(user_course__id = request.user.id)
        context = {"courses":result}
        return render(request, page, context)   


    
class create_course(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.add_course"]
    def get(self, request):
        form = CreateCourse()
        form.fields['add_instructors'].queryset= User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        teacher = User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        teacher_list = list(teacher.values('first_name', 'id'))
        return render(request, 'Create_Course.html', {"form":form, "teacher":teacher_list})
    def post(self, request):
        form = CreateCourse(request.POST, request.FILES)
        print(form.errors)
        if(form.is_valid()):
            print("ถูกต้องเเล้วค้าบบบ")
            teacher = request.POST.getlist('add_instructors')
            course = form.save()
            owner_teacher = User.objects.get(pk=request.user.id)
            course.user_course.add(owner_teacher)
            print(teacher)
            if(teacher != ['']):
                for i in teacher:
                    course.user_course.add(i)
                    course.save()
            return redirect('show_course')
        return render(request, 'Create_Course.html')


class edit_course(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        form = EditCourse(instance=course)
        teacher_incourse = User.objects.filter(course__id = course_id)
        return render(request, 'Edit_Course.html', {"form":form, "course":course, "teachers":teacher_incourse})
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        form = EditCourse(request.POST, request.FILES,instance=course)
        if(form.is_valid()):
            form.save()
            add_teacher = request.POST.getlist('add_instructors')
            del_teacher = request.POST.getlist('del_instructors')
            print(add_teacher)
            print(del_teacher)
        if(len(add_teacher)  > 0 and add_teacher != ['']):
                print('เข้าadd')
                for i in add_teacher:
                    course.user_course.add(i)
                    course.save()
        if(len(del_teacher)  > 0 and del_teacher != ['']):
                print('เข้าdel')
                print(del_teacher)
                splitlist = str(del_teacher).split(',')
                print(splitlist)                
                true_teacher_list = []
                for item in splitlist:
                    true_value = item.strip().replace("'", "").replace("[", "").replace("]", "")
                    if true_value:
                        true_teacher_list.append(int(true_value))
                for i in true_teacher_list:
                    print(i)
                    if(i != ''):
                        del_t = User.objects.get(pk=i)
                        course.user_course.remove(del_t)
                        course.save()        
                return render(request, 'show_selected_course.html',{"course":course})
        return render(request, 'Edit_Course.html', {"form":form, "course":course})

    

class create_topic(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        form = CreateTopic()
        print("เข้า get")
        return render(request, 'Create_Topic.html',{"form":form, "course_id":course_id})
    def post(self, request, course_id):
        form = CreateTopic(request.POST, request.FILES)
        if(form.is_valid()):
            course = Course.objects.get(pk=course_id)
            content = Content.objects.create(course = course, content_name= form.cleaned_data['content_name'], description = form.cleaned_data['description'])
            files = request.FILES.getlist('file_path')
            videos = request.POST.getlist('video_url')
            for file in files:
                material = Material.objects.create(content=content, file_path = file, video_url = "")
                material.save()
            for video in videos:
                emvideo = video.replace('/watch?v=', '/embed/')
                print(emvideo)
                material = Material.objects.create(content=content, file_path = "", video_url = emvideo)
            return render(request, 'show_selected_course.html',{"course":course})   #redirect ให้มัน refresh หน้าใหม่
        return render(request, 'Create_Topic.html',{"form":form, "course_id":course_id})        

class edit_topic(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Edit_Topic.html')

class profile(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        print(request.user.user_info.profile_image)
        return render(request, 'Profile.html')
    
class view_description (View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        context = {"course":course}
        return render(request, 'view_description.html', context)
    
class enroll(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        student = User.objects.get(pk=request.user.id)
        student.course_set.add(course)
        context = {"course":course}
        return render(request, 'show_selected_course.html', context)
    
class quit(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        student = User.objects.get(pk=request.user.id)
        student.course_set.remove(course)
        return redirect('show_course')
    
class Course_Detail(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        # incourse = เช็คว่าอยู่ใน course ไหม
        incourse = Course.objects.filter(pk=course_id, user_course = request.user)
        course = Course.objects.get(pk=course_id)
        content = Content.objects.filter(course = course)
        print(content)
        context = {"course": course, "contents":content}
        print(incourse)
        # exists เอาไว้เช็คว่าที่ filter นั้นมีข้อมูลไหม
        if(incourse.exists()):
            print('incourse')
            return render(request, 'show_selected_course.html', context)
        # อย่าลืม teacher
        return render(request, 'view_description.html', context)


class Changepassword(View):
    def get(self, request):
        form = Changepasswordform(request.user)
        return render(request, 'Change.html', {"form": form})
    
    def post(self, request):
        form = Changepasswordform(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.save
            messages.success(request, 'เปลี่ยนรหัสผ่านสำเร็จ กรุณา Login ใหม่อีกครั้ง')  
            return redirect('Login')
        return render(request, 'Change.html', {"form": form})    



class Register(View):
    def get(self, request):
        print('yahaloooo')
        form = Registerform()
        return render(request, 'Register.html', {"form": form})
    
    def post(self, request):
        form = Registerform(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='Student')
            User_Info.objects.create(user = user, role="Student", profile_image= form.cleaned_data['profile_image'])
            user.groups.add(group)
            user.save()
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
        return redirect('show_course')
    


class Student_List(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):

        student = User.objects.filter(course__id = course_id, user_info__role = "Student")
        print(student)
        context = {"students":student}
        return render(request, 'student_list.html', context)
    

class teacher_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        quiz = Quiz.objects.filter(course = course)
        return render(request, 'teacher_quiz.html', {'quiz': quiz, 'course': course})
    
class teacher_quiz_detail(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        quiz = Quiz.objects.filter(course = course)
        return render(request, 'teacher_quiz_detail.html', {'quiz': quiz})
    
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

            return redirect('teacher_quiz', course_id)

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
        quiz = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.filter(quiz = quiz)
        return render(request, 'Question_list.html', {'quiz': quiz, 'question': question})


class edit_question(View):

    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        questionform = AddQuestionForm(instance=question, initial={'question_name': question.question_name, 'point': question.point})
        if question.question_type == 'Choice':
            all_choice = Choice.objects.filter(question = question)
            # num_choice = all_choice.count()
            ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=0)
            formset = ChoiceFormSet(queryset=all_choice)
            return render(request, 'edit_question.html', {'question': question, 'questionform': questionform, 'formset': formset})
        elif question.question_type == 'Text':
            return render(request, 'edit_question.html', {'question': question, 'questionform': questionform})
    
    def post(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        questionform = AddQuestionForm(request.POST)

        if questionform.is_valid():
            question.question_name = questionform.cleaned_data['question_name']
            question.point = questionform.cleaned_data['point']
            question.save()

            if question.question_type == 'Choice':
                ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=10)
                formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

                if formset.is_valid():
                    choice = Choice.objects.filter(question = question)
                    choice.delete()

                    for form in formset:
                        c = form.save(commit=False)
                        c.question = question
                        c.save()

                    return redirect('question_list', question.quiz.id)
                    
                print(formset.errors)
                return render(request, 'edit_question.html', {'question': question, 'questionform': questionform, 'formset': formset})

            return redirect('question_list', question.quiz.id)
        
        if question.question_type == 'Choice':
            ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm)
            formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

            return render(request, 'edit_question.html', {'question': question, 'questionform': questionform, 'formset': formset})
        
        return render(request, 'edit_question.html', {'question': question, 'questionform': questionform})

