from django.shortcuts import render

from materials.models import Material


def material_page(request):
    return render(request, "material.html")


def tasks_page(request):
    materials = Material.objects.values("name", "id")
    return render(request, "tasks.html", context={"materials": materials})
