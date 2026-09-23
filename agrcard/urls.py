from django.urls import path

from agrcard.soap_server import django_soap_application

urlpatterns = [
    path("soap/", django_soap_application, name="agrcard-soap")
]
