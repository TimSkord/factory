# Generated by Django 4.2.3 on 2023-07-23 18:26

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("materials", "0002_alter_material_byproducts_alter_material_made_of"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="material",
            name="byproducts",
        ),
    ]
