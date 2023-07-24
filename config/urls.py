"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path

from materials.views import (
    MaterialsAPIView,
    material_page,
    produce_material,
    celery_produce_material,
    get_task_info,
    get_tasks_info,
    tasks_page,
    tasks_stop,
    ActiveTaskIDsView,
    MaterialList,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('material/', material_page),
    path('api/materials/', MaterialsAPIView.as_view()),
    path('api/materials/<int:material_id>/produce', produce_material),
    path('api/materials/tasks/<int:material_id>/produce', celery_produce_material),
    path('api/materials/tasks/<str:task_id>/info', get_task_info),
    path('api/materials/tasks/info', get_tasks_info),
    path('tasks/', tasks_page),
    path('api/tasks/<str:task_id>/stop/', tasks_stop),
    path('api/materials/', MaterialList.as_view(), name='material_list'),
    path('active-task-ids/', ActiveTaskIDsView.as_view(), name='active-task-ids'),
]
