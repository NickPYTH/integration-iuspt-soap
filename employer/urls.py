from django.urls import path

from employer.soap_server import django_soap_application

urlpatterns = [
    path("soap/", django_soap_application, name="employer-soap")
]
