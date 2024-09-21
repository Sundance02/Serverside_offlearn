from datetime import *
from django import forms
from .models import *
from django.forms import ModelForm, ValidationError

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

    # def clean_hire_date(self):
    #     data = self.cleaned_data["hire_date"]
    #     if data > date.today():
    #         raise ValidationError("Invalid Date")
    #     return data

# class ProjectForm(ModelForm):

#     due_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
#     start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))

#     class Meta:
#         model = Project
#         fields = ['name', 'manager', 'due_date', 'start_date', 'description']
    
#     def clean(self):
#         clean_data = super().clean()
#         start = self.cleaned_data['start_date']
#         due = self.cleaned_data['due_date']
        
#         if start >= due:
#             raise ValidationError("Error Date")
        
#         return clean_data

# class EditProjectForm(ModelForm):
    
#     due_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))
#     start_date = forms.DateField(widget=forms.TextInput(attrs={"type": "date"}))

#     class Meta:
#         model = Project
#         fields = ['name', 'start_date', 'due_date', 'description', 'manager', 'staff']
    
#     def clean(self):
#         clean_data = super().clean()
#         start = self.cleaned_data['start_date']
#         due = self.cleaned_data['due_date']
        
#         if start >= due:
#             raise ValidationError("Error Date")
        
#         return clean_data