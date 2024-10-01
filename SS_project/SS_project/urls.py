from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from offlearn.views import Login, Register, Logout, Changepassword

urlpatterns = [
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path("offlearn/", include("offlearn.urls")),
    path("Login/", Login.as_view(), name="Login"),
    path("Register/", Register.as_view(), name="Register"),
    path("logout/", Logout.as_view(), name="Logout"),
    path("Changepassword/", Changepassword.as_view(), name="Changepassword"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)