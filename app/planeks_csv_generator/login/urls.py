from django.urls import path

from planeks_csv_generator.login.views import LoginView

urlpatterns = [
    path("", LoginView.as_view()),
]