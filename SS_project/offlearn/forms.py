from datetime import *
from django import forms
from .models import *
from django.forms import ModelForm, ValidationError
from django.forms import ModelForm, DateField, Textarea
from django.forms.widgets import TextInput, Textarea, PasswordInput
from django.core.exceptions import ValidationError
from datetime import date
from django import forms
from offlearn.models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class AddQuizForm(ModelForm):

    name = forms.CharField(widget=forms.TextInput(attrs={"class": "bg-gray-200 rounded-md px-3 py-2 w-[70%]", "placeholder": "Enter Quiz name"}))
    max_point = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "placeholder": "Enter Score"}))
    deadline = forms.DateTimeField(widget=forms.DateTimeInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "type": "datetime-local"}))
    
    class Meta:
        model = Quiz
        fields = ['name', 'max_point', 'deadline']


class AddQuestionForm(ModelForm):

    question_name = forms.CharField(widget=forms.Textarea(attrs={"class": "bg-gray-200 rounded-md px-3 py-2 w-[70%]", "placeholder": "Enter Question", "rows": "4"}))
    point = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "bg-gray-200 border rounded-md px-3 py-2 w-[15%]", "placeholder": "Enter Score"}))
    
    class Meta:
        model = Question
        fields = ['question_name', 'point']


class AddChoiceForm(ModelForm):

    choice_name = forms.CharField(widget=forms.TextInput(attrs={"class": "rounded-md bg-gray-200", "placeholder": "Enter Choice"}))
    is_correct = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "bg-gray-200 border rounded-md", "placeholder": "Enter Score"}))
    
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
    # ยังไม่ได้ทำรูป

    class Meta:
        model = User
        fields = [
            "username",
            "first_name", 
            "last_name", 
            "password1",
            "password2",
            "email",
        ]
