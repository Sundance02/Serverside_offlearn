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
from django.db.models import Sum



class show_course(View):
    def get(self, request):
        user_course = Course.objects.filter(user_course__id = request.user.id)
        if(request.user.groups.filter(name="Student").exists()):
            role = "Student"
        elif(request.user.groups.filter(name="Instructor").exists()):
            role = "Teacher"
        elif(request.user.groups.filter(name="Admin").exists()):
            role = "Admin"
            user_course = Course.objects.all() 
        else:
            role = "Guest"
            user_course = Course.objects.all() 
        context = {"courses":user_course, "role":role}
        return render(request, "Allcourse.html", context)  


        
class searched_course(View):
    # post เอาไว้ใช้กับ search
    def post(self, request):
        if(request.user.groups.filter(name="Student").exists()):
            role = "Student"
        elif(request.user.groups.filter(name="Instructor").exists()):
            role = "Teacher"
        elif(request.user.groups.filter(name="Admin").exists()):
            role = "Admin"
        else:
            role = "Guest"
        searched_info = request.POST['searched']
        if role != "Teacher":
            result = Course.objects.filter(course_name__icontains = searched_info)
        else:
            result = Course.objects.filter(course_name__icontains = searched_info, user_course__id = request.user.id)

        context = {"courses":result, "role":role}
        return render(request, 'Allcourse.html', context)
    
    # getเอาไว้ใช้กับปุ่ม filter
    def get(self, request):
        result = ""       
        if(request.user.groups.filter(name="Student").exists()):
            role = "Student"
        elif(request.user.groups.filter(name="Instructor").exists()):
            role = "Teacher"
        elif(request.user.groups.filter(name="Admin").exists()):
            role = "Admin"
        else:
            role = "Guest"

        filter = request.GET.get('filter')
        if(filter == "all"):
            result = Course.objects.all()
        elif(filter == "own"):
            result = Course.objects.filter(user_course__id = request.user.id)
        elif(filter == "notown"):
            result = Course.objects.exclude(user_course__id = request.user.id)
        context = {"courses":result, "role":role}
        return render(request, 'Allcourse.html', context)   


    
class create_course(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/Login/'
    permission_required = ["offlearn.add_course"]
    def get(self, request):
        form = CreateCourse()
        teacher = User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        teacher_list = list(teacher.values('username', 'id'))
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
            # เพิ่ม admin ที่เป็นคนดูเเลระบบ 
            admin = User.objects.filter(user_info__role = "Admin")
            for i in admin:
                course.user_course.add(i)
            if(teacher):
                for i in teacher:
                    course.user_course.add(i)
                    course.save()
            return redirect('show_course')
        teacher = User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        teacher_list = list(teacher.values('username', 'id'))
        return render(request, 'Create_Course.html', {"form":form, "teacher":teacher_list})


class edit_course(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.change_course"]
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        form = CreateCourse(instance=course)
        all_teacher = User.objects.filter(user_info__role="Instructor").exclude(course__id = course_id, user_info__role="Instructor")
        all_teacher_list = list(all_teacher.values('username', 'id'))
        # query อจ ที่อยู่ในคอร์สทั้งหมด
        teacher_incourse = User.objects.filter(course__id = course_id, user_info__role="Instructor")
        return render(request, 'Edit_Course.html', {"form":form, "course":course, "teachers":teacher_incourse, "all_teacher":all_teacher_list})
    def post(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        form = CreateCourse(request.POST, request.FILES,instance=course)
        print("เข้า post")
        if(form.is_valid()):
            print('เเก้ไขคอร์สเข้า valid')
            form.save()
            add_teacher = request.POST.getlist('add_instructors')
            del_teacher = request.POST.getlist('del_instructors')
            print(add_teacher)
            print("1)", del_teacher)
            if(add_teacher):
                    print('เข้าadd')
                    for i in add_teacher:
                        course.user_course.add(i)
                        course.save()
            if(del_teacher):
                    print('เข้าdel')
                    splitlist = str(del_teacher).split(',')
                    print("2)", splitlist)                
                    true_teacher_list = []
                    for item in splitlist:
                        print("3)", item)
                        true_value = item.strip().replace("'", "").replace("[", "").replace("]", "")
                        print("4)", true_value)
                        if true_value:
                            true_teacher_list.append(int(true_value))
                    for i in true_teacher_list:
                        print("5)", i)
                        if(i != ''):
                            del_t = User.objects.get(pk=i)
                            course.user_course.remove(del_t)
                            course.save()
                    return redirect('Course_Detail', course_id=course.id)
        form.fields['add_instructors'].queryset= User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        all_teacher = User.objects.filter(user_info__role="Instructor").exclude(pk=request.user.id)
        all_teacher_list = list(all_teacher.values('username', 'id'))
        teacher_incourse = User.objects.filter(course__id = course_id)
        return render(request, 'Edit_Course.html', {"form":form, "course":course, "teachers":teacher_incourse, "all_teacher":all_teacher_list})

    
class delete_course(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/Login/'
    permission_required = ["offlearn.delete_course"]
    def get(self, request, course_id):
        course = Course.objects.get(pk = course_id)
        course.delete()
        return redirect('show_course')  #redirect ให้มัน refresh หน้าใหม่


class create_topic(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/Login/'
    permission_required = ["offlearn.add_content"]
    def get(self, request, course_id):
        form = CreateTopic()
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
            return redirect('Course_Detail', course_id=course.id)  #redirect ให้มัน refresh หน้าใหม่
        return render(request, 'Create_Topic.html',{"form":form, "course_id":course_id})

class edit_topic(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.change_content"]
    def get(self, request, topic_id):
        content = Content.objects.get(pk=topic_id)
        course = Course.objects.get(pk = content.course.id)
        material = Material.objects.filter(content = content)
        form = CreateTopic(instance=content)
        return render(request, 'Edit_Topic.html', {'form':form, "contents":content, "materials":material, "course":course})
    
    def post(self, request, topic_id):
        content = Content.objects.get(pk=topic_id)
        material = Material.objects.filter(content = content)
        form = CreateTopic(request.POST, request.FILES, instance=content)
        courseid = content.course.id
        print('รอvalid')
        print(form.errors.as_text)
        if(form.is_valid()):
            print('valid')
            form.save()
            del_video = request.POST.getlist('del_video')
            del_file = request.POST.getlist('del_file_path')
            add_video = request.POST.getlist('video_url')
            add_file = request.FILES.getlist('file_path')
            print(del_file)
            print(del_video)
            # delete section
            videoSplitList = str(del_video).split(',')
            fileSplitList = str(del_file).split(',')

            trueVideoList = []
            trueFileList = []

 
            if(del_file):
                fileSplitList = str(del_file).split(',')
                trueFileList = []
                for file in fileSplitList:
                    true_value = file.strip().replace("'", "").replace("[", "").replace("]", "")
                    if true_value:
                        trueFileList.append(int(true_value))
                for file in trueFileList:
                    if(file != ''):                        
                        file = Material.objects.get(pk=file)
                        file.delete()
            

            if(del_video):
                videoSplitList = str(del_video).split(',')
                trueVideoList = []
                for video in videoSplitList:
                    true_value = video.strip().replace("'", "").replace("[", "").replace("]", "")
                    if true_value:
                        trueVideoList.append(int(true_value))
                for video in trueVideoList:
                    if(video != ''):
                        print(video)
                        video = Material.objects.get(pk=video)
                        video.delete()

            # add section
            if(add_file):
                for file in add_file:
                    file_mat = Material.objects.create(content = content, file_path = file, video_url = '')
            if(add_video):
                for video in add_video:
                    emvideo = video.replace('/watch?v=', '/embed/')
                    video_mat = Material.objects.create(content = content, file_path = "", video_url = emvideo)
            return redirect('Course_Detail', course_id=courseid) 
        return render(request, 'Edit_Topic.html', {"form": form,"contents":content, "materials":material})


class delete_topic(LoginRequiredMixin, PermissionRequiredMixin,View):
    login_url = '/Login/'
    permission_required = ["offlearn.delete_content"]
    def get(self, request, topic_id):
        content = Content.objects.get(pk = topic_id)
        course = Course.objects.get(pk = content.course.id)
        content.delete()
        return redirect('Course_Detail', course_id=course.id)  #redirect ให้มัน refresh หน้าใหม่



class profile(LoginRequiredMixin, View):
    login_url = '/Login/'
    def get(self, request):
        return render(request, 'Profile.html')
    
class view_description (View):
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        teacher = User.objects.filter(user_info__role = 'Instructor', course__id = course_id)
        context = {"course":course, "teacher":teacher}
        return render(request, 'view_description.html', context)
    
class enroll(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.enroll_course"]
    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        student = User.objects.get(pk=request.user.id)
        student.course_set.add(course)
        return redirect('Course_Detail', course_id=course_id) 
    
class quit(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.quit_course"]
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
        context = {"course": course, "contents":content}
        if(incourse.exists()):
            print('อยู่ในคอร์ส')
            return render(request, 'show_selected_course.html', context)
        return redirect('view_description', course_id)


class Changepassword(LoginRequiredMixin, View):
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
        if form.is_valid():
            user = form.save()
            if request.user.has_perm('offlearn.add_instructor'):
                group = Group.objects.get(name='Instructor')
                user.groups.add(group)
                user.save()
                if(form.cleaned_data['profile_image']):
                    User_Info.objects.create(user = user, role= "Instructor", profile_image= form.cleaned_data['profile_image'])
                else:
                    User_Info.objects.create(user = user, role= "Instructor", profile_image= 'default.jpg')
                messages.success(request, 'Account created successfully')  
            else:
                group = Group.objects.get(name='Student')
                user.groups.add(group)
                user.save()
                if(form.cleaned_data['profile_image']):
                    User_Info.objects.create(user = user, role= "Student", profile_image= form.cleaned_data['profile_image'])
                else:
                    User_Info.objects.create(user = user, role= "Student", profile_image= 'default.jpg')
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
            print(request.user.groups.all())
            print(request.user.has_perm('offlearn.add_instructor'))
            return redirect('show_course')
        return render(request, 'Login.html', {"form": form})

class Logout(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('show_course')
    


class Student_List(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ["offlearn.view_student"]

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        quiz = Quiz.objects.filter(course = course).order_by('id')
        students = User.objects.filter(course__id=course_id, user_info__role="Student").annotate(total_score=Sum('quizscore__score', filter=Q(quizscore__quiz__in = quiz))).order_by('id')
        context = {"students": students, "course_id":course_id, "quiz": quiz}
        return render(request, 'student_list.html', context)
    

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
    

class create_quiz(LoginRequiredMixin, PermissionRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.add_quiz']

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

class edit_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.change_quiz']

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        quizform = AddQuizForm(instance=quiz)
        return render(request, 'edit_quiz.html', {'quizform': quizform, 'quiz': quiz})

    def post(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        quizform = AddQuizForm(request.POST)
        if quizform.is_valid():
            quiz.quiz_name = quizform.cleaned_data['quiz_name']
            quiz.deadline = quizform.cleaned_data['deadline']
            quiz.max_point = quizform.cleaned_data['max_point']
            quiz.save()
            return redirect('teacher_quiz', quiz.course.id)
        return render(request, 'edit_quiz.html', {'quizform': quizform, 'quiz': quiz})

class delete_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.delete_quiz']
    
    def post(self, request, quiz_id):
        if request.POST.get('_method') == 'DELETE':
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz.delete()
            return redirect('teacher_quiz', quiz.course.id)
    

class add_choice_question(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.add_question', 'offlearn.add_choice']

    def get(self, request, quiz_id):

        ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=2) # modelformset_factory สร้าง FormSet (กลุ่มของฟอร์ม) จาก ModelForm ซึ่งช่วยให้คุณสามารถสร้างฟอร์มหลาย ๆ ฟอร์มที่อิงตามโมเดลเดียวกันได้ในครั้งเดียว
        formset = ChoiceFormSet(queryset=Choice.objects.none())
        quiz = Quiz.objects.get(pk=quiz_id)
        return render(request, 'choice_question.html', {'choiceform': formset, 'questionform': AddQuestionForm(), 'quiz': quiz})

    def post(self, request, quiz_id):

        questionform = AddQuestionForm(request.POST)
        exist_point = Question.objects.filter(quiz_id = quiz_id).aggregate(total_point = Sum('point'))['total_point'] or 0
        quiz = Quiz.objects.get(pk=quiz_id)
        ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=10)
        formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

        if questionform.is_valid() and formset.is_valid():

            # Point Validation
            if questionform.cleaned_data['point'] + exist_point > quiz.max_point:
                questionform.add_error('point', ValidationError(f"Points exceed the maximum allowed for this quiz. You can add up to {quiz.max_point - exist_point} more points."))
            else:

                for form in formset:
                    if not form.cleaned_data:
                        questionform.add_error(None, ValidationError("You must fill out all forms."))
                        print(questionform.errors)
                        return render(request, 'choice_question.html', {'questionform': questionform, 'choiceform': formset, 'quiz': quiz})

                quest = questionform.save(commit=False)
                quest.quiz = quiz
                quest.save()


                for form in formset:
                    if form.cleaned_data:
                        choice = form.save(commit=False)
                        choice.question = quest
                        choice.save()
                   

                return redirect('question_list', quiz_id)

        # print(formset.errors)
        return render(request, 'choice_question.html', {'questionform': questionform, 'choiceform': formset, 'quiz': quiz})

class add_context_question(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.add_question']

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        form = AddQuestionForm()
        return render(request, 'context_question.html', {'questionform': form, 'quiz': quiz})

    def post(self, request, quiz_id):

        form = AddQuestionForm(request.POST)
        quiz = Quiz.objects.get(pk=quiz_id)
        exist_point = Question.objects.filter(quiz_id = quiz_id).aggregate(total_point = Sum('point'))['total_point'] or 0 # ใช้ or 0 เพื่อถ้า query เป็น None จะเปลี่ยนเป็น 0 แทน

        if form.is_valid():

            # Point Validation
            if form.cleaned_data['point'] + exist_point > quiz.max_point:
                form.add_error('point', ValidationError(f"Points exceed the maximum allowed for this quiz. You can add up to {quiz.max_point - exist_point} more points."))
            else:
                quest = form.save(commit=False)
                quest.quiz = Quiz.objects.get(pk=quiz_id)
                quest.save()
                return redirect('question_list', quiz_id)
        # print(form.errors)
        return render(request, 'context_question.html', {'questionform': form, 'quiz': quiz})


class question_list(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.view_question']

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.filter(quiz = quiz).order_by('id')
        return render(request, 'Question_list.html', {'quiz': quiz, 'question': question})
    

class delete_question(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.delete_question']

    def post(self, request, question_id):
        if request.POST.get('_method') == 'DELETE':
            question = Question.objects.get(pk=question_id)
            question.delete()
            return redirect('question_list', question.quiz.id)


class edit_question(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.change_question']


    def get(self, request, question_id):
        question = Question.objects.get(pk=question_id)
        questionform = AddQuestionForm(instance=question)
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
        exist_point = Question.objects.filter(quiz_id = question.quiz.id).aggregate(total_point = Sum('point'))['total_point'] or 0

        if questionform.is_valid():
            if questionform.cleaned_data['point'] + (exist_point - question.point) > question.quiz.max_point:
                questionform.add_error('point', ValidationError(f"Points exceed the maximum allowed for this quiz. You can add up to {question.quiz.max_point - exist_point} more points."))
            else:

                question.question_name = questionform.cleaned_data['question_name']
                question.point = questionform.cleaned_data['point']
                question.save()

                if question.question_type == 'Choice':
                    ChoiceFormSet = modelformset_factory(Choice, form=AddChoiceForm, extra=10)
                    formset = ChoiceFormSet(request.POST, queryset=Choice.objects.none())

                    if formset.is_valid():

                        for form in formset:
                            if not form.cleaned_data:
                                questionform.add_error(None, ValidationError("You must fill out all forms."))
                                return render(request, 'edit_question.html', {'question': question, 'questionform': questionform, 'formset': formset})

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


class student_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.view_quiz', 'offlearn.view_question', 'offlearn.view_choice']


    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.filter(quiz = quiz).order_by('id')
        student_answer = StudentAnswer.objects.filter(quiz=quiz, student=request.user).first()
        # print(student_answer)
        return render(request, 'student_quiz.html', {'question': question, 'quiz': quiz, 'student_answer': student_answer})
    
    def post(self, request, quiz_id):
        user = User.objects.get(pk=request.user.id)
        quiz = Quiz.objects.get(pk=quiz_id)
        question = Question.objects.filter(quiz = quiz).order_by('id')
        for q in question:
            ans =  request.POST.get(str(q.id))
            if q.question_type == 'Text':
                StudentAnswer.objects.create(quiz = quiz, student = user, question = q, choice = None, text_answer = ans)
            elif q.question_type == 'Choice':
                cc = Choice.objects.get(pk=int(ans))
                StudentAnswer.objects.create(quiz = quiz, student = user, question = q, choice = cc, text_answer = None)
        return redirect("teacher_quiz", quiz.course.id)
    

class teacher_quiz(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.view_quiz']

    def get(self, request, course_id):
        course = Course.objects.get(pk=course_id)
        quiz = Quiz.objects.filter(course = course).order_by('id')
        # stu_answer = StudentAnswer.objects.filter(student=request.user).distinct('quiz')
        # print(stu_answer[1].quiz)
        return render(request, 'quiz_list.html', {'quiz': quiz, 'course': course})


class teacher_quiz_student_list(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.add_student_answer', 'offlearn.view_quiz_score']

    def get(self, request, quiz_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        student_answer = StudentAnswer.objects.filter(quiz=quiz).distinct('student')
        return render(request, 'teacher_quiz_student_list.html', {'quiz': quiz, 'student_answer': student_answer})


class teacher_add_studentscore(LoginRequiredMixin, View):
    login_url = '/Login/'
    permission_required = ['offlearn.add_quizscore']

    def get(self, request, quiz_id, student_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        student = User.objects.get(pk=student_id)
        student_answer = StudentAnswer.objects.filter(quiz=quiz, student=student, choice=None)
        return render(request, 'teacher_add_studentscore.html', {'student_answer': student_answer, 'quiz': quiz, 'student': student})

    def post(self, request, quiz_id, student_id):
        quiz = Quiz.objects.get(pk=quiz_id)
        student = User.objects.get(pk=student_id)
        student_answer = StudentAnswer.objects.filter(quiz=quiz, student=student)
        total_score = 0
        for i in student_answer:
            if i.question.question_type == 'Text':
                text_score = request.POST.get(str(i.id))
                total_score += int(text_score)
            else:
                if i.choice.is_correct:
                    total_score += i.question.point

        qq = QuizScore.objects.create(student = student, quiz = quiz, score = total_score)
        
        for i in student_answer:
            i.score = qq
            i.save()
        
        return redirect('teacher_quiz_student_list', quiz_id)