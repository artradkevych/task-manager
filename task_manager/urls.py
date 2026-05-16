"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from task_manager.settings import prod
from core.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("catalog/", include("catalog.urls", namespace="catalog")),
    path("users/", include("users.urls", namespace="users")),
    path("work/", include("work.urls", namespace="work")),
    path("accounts/", include("django.contrib.auth.urls")),
] + static(prod.STATIC_URL, document_root=prod.STATIC_ROOT)
