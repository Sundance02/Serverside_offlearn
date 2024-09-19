from django.urls import path
from offlearn import views
urlpatterns = [
    path("show_course_guest/", views.show_course_guest.as_view(), name="show_course_guest"),
    path("show_course_student/", views.show_course_student.as_view(), name="show_course_student"),
    path("show_course_teacher/", views.show_course_teacher.as_view(), name="show_course_teacher"),
    path("create_course/", views.create_course.as_view(), name="create_course"),
    path("edit_course/", views.edit_course.as_view(), name="edit_course"),
    path("create_topic/", views.create_topic.as_view(), name="create_topic"),
    path("edit_topic/", views.edit_topic.as_view(), name="edit_topic"),
    path("profile/", views.profile.as_view(), name="profile"),
    path("view_description/", views.view_description.as_view(), name="view_description"),
    path("Register/", views.Register.as_view(), name="Register"),
    path("Login/", views.Login.as_view(), name="Login"),
    path("Course_Detail_student/", views.Course_Detail_student.as_view(), name="Course_Detail_student"),
    path("Course_Detail_teacher/", views.Course_Detail_teacher.as_view(), name="Course_Detail_teacher"),
    path("student_list/", views.Student_List.as_view(), name="student_list"),
    path("teacher_quiz/", views.teacher_quiz.as_view(), name="teacher_quiz"),
    path("teacher_quiz_detail/", views.teacher_quiz_detail.as_view(), name="teacher_quiz_detail"),
    path("student_quiz/", views.student_quiz.as_view(), name="student_quiz"),
]

