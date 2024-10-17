from datetime import *
from django.utils import timezone
from django import forms
from .models import *
from django.forms import ModelForm, ValidationError
from django.forms import ModelForm, DateField, Textarea
from django.forms.widgets import TextInput, Textarea, PasswordInput
from django.core.exceptions import ValidationError
from offlearn.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm


class AddQuizForm(ModelForm):

    quiz_name = forms.CharField(widget=forms.TextInput(attrs={"class": "bg-gray-200 rounded-md px-3 py-2 w-[70%]", "placeholder": "Enter Quiz name"}))
    max_point = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "placeholder": "Enter Score"}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "type": "datetime-local"}))
    
    class Meta:
        model = Quiz
        fields = ['quiz_name', 'max_point', 'deadline']

    def clean_deadline(self):
        data = self.cleaned_data.get('deadline')
        current_datetime = timezone.now()
        if data <= current_datetime:
            raise ValidationError("The deadline date and time must not be in the past.")

        return data


class AddQuestionForm(ModelForm):

    question_name = forms.CharField(widget=forms.Textarea(attrs={"class": "bg-gray-200 rounded-md px-3 py-2 w-[70%]", "placeholder": "Enter Question", "rows": "4"}))
    point = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "placeholder": "Enter Score"}))
    
    class Meta:
        model = Question
        fields = ['question_name', 'point', 'question_type']


class AddChoiceForm(ModelForm):

    choice_name = forms.CharField(widget=forms.TextInput(attrs={"class": "rounded-md bg-gray-200", "placeholder": "Enter Choice"}))
    is_correct = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={"class": "bg-gray-200 border rounded-md"}))
    
    class Meta:
        model = Choice
        fields = ['choice_name', 'is_correct']


class Registerform(UserCreationForm):
    first_name = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4 w-[700px]"}))
    last_name = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4"}))
    password1 = forms.CharField(widget=PasswordInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4 w-[700px]"}))
    password2 = forms.CharField(widget=PasswordInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4 w-[700px]"}))
    email = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4"}))
    username = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4 w-[700px]"}))
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = [
            "username",
            "first_name", 
            "last_name", 
            "password1",
            "password2",
            "email",
            "profile_image"
        ]

class Loginform(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"ชื่อผู้ใช้..." }))
    password = forms.CharField(widget=PasswordInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"รหัสผ่าน..."}))

    class Meta:
        model = User
        fields = [
            "username",
            "password"
        ]


class Changepasswordform(SetPasswordForm):
    new_password1 = forms.CharField(widget=PasswordInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"รหัสผ่านใหม่"}))
    new_password2 = forms.CharField(widget=PasswordInput(attrs={"class":"block bg-white w-full border border-slate-300 rounded-md w-[350px] py-2 px-4", "placeholder":"ยืนยันรหัสผ่าน"}))

    class Meta:
        model = User
        fields = [
            "new_password1",
            "new_password2"
        ]


class CreateCourse(ModelForm):
    course_name = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4"}), max_length=80 , required=False)
    course_description = forms.CharField(widget=Textarea(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-lg text-base py-2 px-4", "rows":"5", "cols":"30"}), max_length=255 , required=False)
    course_image = forms.ImageField()
    # ลบเอาไว้ใช้กับเเก้ไขคอร์ส
    del_instructors = forms.ModelChoiceField( queryset= User.objects.filter(user_info__role="Instructor" ), required=False, widget=forms.HiddenInput(attrs={"id":"del_instructors"}))
    class Meta:
        model = Course
        fields = [
            "course_name",
            "course_description",
            "course_image"
        ]
    def clean_course_name(self):
        course_name = self.cleaned_data.get('course_name')
        if not course_name:
            raise forms.ValidationError("กรุณากรอกชื่อคอร์ส")
        return course_name

    def clean_course_description(self):
        course_description = self.cleaned_data.get('course_description')
        if not course_description:
            raise forms.ValidationError("กรุณากรอกคำอธิบายคอร์ส")
        return course_description


BLACKLISTED_EXTENSIONS = ['.exe', '.bat', '.cmd', '.js', '.sh']

class CreateTopic(ModelForm):
    content_name = forms.CharField(widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4"}), max_length=80, required=False)
    description = forms.CharField(widget=Textarea(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-lg text-base py-2 px-4", "rows":"5", "cols":"30"}), max_length=255, required=False)
    video_url = forms.CharField(required=False, widget=TextInput(attrs={"class":"bg-[#F4F4F4] col-span-3 rounded-full text-base py-2 px-4"}))
    file_path = forms.FileField(required=False)
    # ลบเอาไว้ใช้กับเเก้ไขtopic
    del_video = forms.CharField(required=False, widget=forms.HiddenInput(attrs={"id":"del_video"}))
    del_file_path = forms.CharField(required=False, widget=forms.HiddenInput(attrs={"id":"del_file_path"}))
    class Meta:
        model = Material
        fields = [
            'file_path',
            'video_url'
        ]

    
    def clean_file_path(self):
        file = self.cleaned_data.get('file_path')
        if file:
            extension = file.name.split('.')[-1].lower()
            print(extension)
            if f".{extension}" in BLACKLISTED_EXTENSIONS:
                raise forms.ValidationError(f"***ไฟล์ชนิด {extension} ไม่ได้รับอนุญาตให้อัปโหลด")
        return file
    
    def clean_content_name(self):
        content_name = self.cleaned_data.get('content_name')
        if not content_name:
            raise forms.ValidationError("กรุณากรอกชื่อเนื้อหา")
        return content_name

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if not description:
            raise forms.ValidationError("กรุณากรอกคำอธิบายเนื้อหา")
        return description
    

