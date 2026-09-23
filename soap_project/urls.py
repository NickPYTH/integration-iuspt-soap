from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("zeep_client/", include("zeep_client.urls")),
    path("edovendor/", include("edovendor.urls")),
    path("agrcard/", include("agrcard.urls")),
    path("employer/", include("employer.urls")),
    path("department/", include("department.urls")),
    path("", include("soap_app.urls")),

]
