from django.urls import path
from offlearn import views
urlpatterns = [
    path("show_course_guest/", views.show_course_guest.as_view(), name="show_course_guest"),
]
