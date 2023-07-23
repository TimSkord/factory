from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Material
from rest_framework import status


class MaterialAPIView(APIView):
    def get(self, request, *args, **kwargs):
        try:
            material = Material.objects.first()
            if material is not None:
                return Response({'name': material.name, 'count': material.count}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'No material found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def material_page(request):
    return render(request, 'material.html')  # material.html - это ваш HTML шаблон
