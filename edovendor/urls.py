from django.urls import path

from edovendor.soap_server import django_soap_application

urlpatterns = [
    path("soap/", django_soap_application, name="edovendor-soap")
]