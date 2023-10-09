from time import sleep

from celery import current_task
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.db import transaction
from django.db.models import F

from .models import Material


@shared_task(bind=True)
def produce_material_task(self, material_id, count):
    material = Material.objects.get(id=material_id)
    all_manufactures = material.made_of.select_related("material").all()
    # r.lpush('tasks', self.request.id)
    Material.objects.filter(pk=material.pk).update(status=True)

    progress_recorder = ProgressRecorder(self)

    for i in range(count):
        with transaction.atomic():
            for manufacture in all_manufactures:
                manufacture.material.count = F("count") - manufacture.cost
                manufacture.material.save(update_fields=["count"])

            sleep(material.manufacturing_time)

        material.count = F("count") + 1
        material.save(update_fields=["count"])

        progress_recorder.set_progress(i + 1, count)
        current_task.update_state(
            state="PROGRESS",
            meta={
                "id": self.request.id,
                "task": f"{material.name} production",
                "progress": ((i + 1) / count) * 100,
                "produced": count,
            },
        )
    Material.objects.filter(pk=material.pk).update(status=False)
    # r.lrem('tasks', 0, self.request.id)
