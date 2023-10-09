from time import sleep

from django.db import models
from django.db.models import F


class Material(models.Model):
    name = models.CharField(max_length=300)
    made_of = models.ManyToManyField(
        "Manufacture", null=True, blank=True, related_name="products"
    )
    count = models.FloatField(default=0)
    manufacturing_time = models.FloatField(default=0.1)
    status = models.BooleanField(default=False)

    def produce(self, count):
        all_manufactures = self.made_of.select_related("material").all()

        Material.objects.filter(pk=self.pk).update(status=True)

        for _ in range(count):
            # with transaction.atomic():
            for manufacture in all_manufactures:
                manufacture.material.count = F("count") - manufacture.cost
                manufacture.material.save(update_fields=["count"])

            sleep(self.manufacturing_time)

            self.count = F("count") + 1
            self.save(update_fields=["count"])

        Material.objects.filter(pk=self.pk).update(status=False)

    def __str__(self):
        return self.name


class Manufacture(models.Model):
    material = models.ForeignKey(
        Material, on_delete=models.CASCADE, related_name="in_process"
    )
    cost = models.FloatField(default=1)

    def __str__(self):
        return f"{self.cost} of {self.material}"
