from django.urls import path
from offlearn import views
urlpatterns = [
    path("", views.show_course.as_view(), name="show_course"),
    path("create_course/", views.create_course.as_view(), name="create_course"),
    path("edit_course/", views.edit_course.as_view(), name="edit_course"),
    path("create_topic/", views.create_topic.as_view(), name="create_topic"),
    path("edit_topic/", views.edit_topic.as_view(), name="edit_topic"),
    path("profile/", views.profile.as_view(), name="profile"),
    path("view_description/<int:course_id>", views.view_description.as_view(), name="view_description"),
    path("Course_Detail/<int:course_id>", views.Course_Detail.as_view(), name="Course_Detail"),
    path("student_list/<int:course_id>", views.Student_List.as_view(), name="student_list"),
    path("teacher_quiz/", views.teacher_quiz.as_view(), name="teacher_quiz"),
    path("teacher_quiz_detail/", views.teacher_quiz_detail.as_view(), name="teacher_quiz_detail"),
    path("student_quiz/", views.student_quiz.as_view(), name="student_quiz"),
    path("student_quiz_answer/", views.student_quiz_answer.as_view(), name="student_quiz_answer"),
    path("student_quiz_detail/", views.student_quiz_detail.as_view(), name="student_quiz_detail"),
    path("create_quiz/", views.create_quiz.as_view(), name="create_quiz"),
    path("add_choice_question/", views.add_choice_question.as_view(), name="add_choice_question"),
    path("add_choice/", views.add_choice.as_view(), name="add_choice"),
    path("add_context_question/", views.add_context_question.as_view(), name="add_context_question"),
    path("searched/", views.searched_course.as_view(), name="searched"),
    path("enroll/<int:course_id>", views.enroll.as_view(), name="enroll"),
    path("quit/<int:course_id>", views.quit.as_view(), name="quit"),

]

