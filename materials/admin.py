from django.contrib import admin

from materials.models import *


def produce_1(modeladmin, request, queryset):
    for material in queryset:
        material.produce(1)


def produce_5(modeladmin, request, queryset):
    for material in queryset:
        material.produce(5)


def produce_10(modeladmin, request, queryset):
    for material in queryset:
        material.produce(10)


def produce_50(modeladmin, request, queryset):
    for material in queryset:
        material.produce(50)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'count', 'manufacturing_time', 'status')
    list_display_links = ('name',)
    actions = (produce_1, produce_5, produce_10, produce_50)


admin.site.register(Manufacture)
