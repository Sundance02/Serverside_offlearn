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