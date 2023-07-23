from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Material


class MaterialsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            materials = Material.objects.all()
            data = [{'name': m.name, 'count': m.count, 'id': m.id} for m in materials]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def material_page(request):
    return render(request, 'material.html')  # material.html - это ваш HTML шаблон


@csrf_exempt
def produce_material(request, material_id):
    if request.method == 'POST':
        count = request.POST.get('count')
        if count is None:
            return JsonResponse({'error': 'Не указано количество для производства'}, status=400)
        try:
            count = int(count)
        except ValueError:
            return JsonResponse({'error': 'Неверное количество для производства'}, status=400)
        if count <= 0:
            return JsonResponse({'error': 'Количество для производства должно быть больше нуля'}, status=400)

        material = get_object_or_404(Material, pk=material_id)

        try:
            material.produce(count)
        except AssertionError:
            return JsonResponse({'error': 'Недостаточно материалов для производства'}, status=400)

        return JsonResponse({'success': True})

    else:
        return JsonResponse({'error': 'Недопустимый метод запроса'}, status=405)
