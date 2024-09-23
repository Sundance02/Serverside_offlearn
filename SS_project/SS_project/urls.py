from django.contrib import admin
from django.urls import path, include
from offlearn.views import Login, Register

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("offlearn/", include("offlearn.urls")),
    path("Login/", Login.as_view(), name="Login"),
    path("Register/", Register.as_view(), name="Register"),

]
