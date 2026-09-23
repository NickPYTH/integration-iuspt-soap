from django.urls import path

from department.soap_server import django_soap_application

urlpatterns = [
    path("soap/", django_soap_application, name="department-soap")
]
