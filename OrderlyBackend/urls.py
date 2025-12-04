# OrderlyBackend/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("UserAuth.urls")),
    path("api/", include("ManageData.urls")),
]