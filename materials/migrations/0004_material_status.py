# Generated by Django 4.2.3 on 2023-07-23 20:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('materials', '0003_remove_material_byproducts'),
    ]

    operations = [
        migrations.AddField(
            model_name='material',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
