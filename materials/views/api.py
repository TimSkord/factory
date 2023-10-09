from celery.result import AsyncResult
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from config.celery import app
from config.redis import r
from materials.models import Material
from materials.serializers import MaterialSerializer
from materials.tasks import produce_material_task


class MaterialsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            materials = Material.objects.all()
            data = [
                {"name": m.name, "count": m.count, "id": m.id, "status": m.status}
                for m in materials
            ]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@csrf_exempt
def produce_material(request, material_id):
    if request.method == "POST":
        count = request.POST.get("count")
        if count is None:
            return JsonResponse(
                {"error": "Не указано количество для производства"}, status=400
            )
        try:
            count = int(count)
        except ValueError:
            return JsonResponse(
                {"error": "Неверное количество для производства"}, status=400
            )
        if count <= 0:
            return JsonResponse(
                {"error": "Количество для производства должно быть больше нуля"},
                status=400,
            )

        material = get_object_or_404(Material, pk=material_id)

        try:
            material.produce(count)
        except AssertionError:
            return JsonResponse(
                {"error": "Недостаточно материалов для производства"}, status=400
            )

        return JsonResponse({"success": True})

    else:
        return JsonResponse({"error": "Недопустимый метод запроса"}, status=405)


def celery_produce_material(request, material_id):
    count = int(request.POST.get("count"))
    task = produce_material_task.delay(material_id, count)
    return JsonResponse({"task_id": task.task_id})


def get_task_info(request, task_id):
    task = AsyncResult(task_id)
    info = task.info if task.state == "PROGRESS" else {}
    return JsonResponse(
        {
            "id": info.get("id"),
            "task": info.get("task"),
            "task_state": task.state,
            "progress": info.get("progress"),
            "produced": info.get("produced"),
        }
    )


def get_tasks_info(request):
    task_ids = [task_id.decode("utf-8") for task_id in r.lrange("tasks", 0, -1)]
    tasks_info = []
    for task_id in task_ids:
        task = AsyncResult(task_id)
        info = task.info if task.state == "PROGRESS" else {}
        tasks_info.append(
            {
                "id": info.get("id"),
                "task": info.get("task"),
                "task_state": task.state,
                "progress": info.get("progress"),
                "produced": info.get("produced"),
            }
        )
    return JsonResponse({"tasks": tasks_info})


class ActiveTaskIDsView(View):
    def get(self, request):
        task_ids = [task_id.decode("utf-8") for task_id in r.lrange("tasks", 0, -1)]
        return JsonResponse({"active_task_ids": task_ids})


def tasks_stop(request, task_id):
    app.control.revoke(task_id, terminate=True)
    r.lrem("tasks", 1, task_id)
    return JsonResponse({"stopped": task_id})


class MaterialList(generics.ListAPIView):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
