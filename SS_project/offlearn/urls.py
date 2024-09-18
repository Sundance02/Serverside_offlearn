from django.urls import path
from offlearn import views
urlpatterns = [
    path("show_course_guest/", views.show_course_guest.as_view(), name="show_course_guest"),
    path("create_course/", views.create_course.as_view(), name="create_course"),
    path("edit_course/", views.edit_course.as_view(), name="edit_course"),
]
