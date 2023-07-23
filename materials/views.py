from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Material
from rest_framework import status


class MaterialsAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            materials = Material.objects.all()
            data = [{'name': m.name, 'count': m.count} for m in materials]
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def material_page(request):
    return render(request, 'material.html')  # material.html - это ваш HTML шаблон
