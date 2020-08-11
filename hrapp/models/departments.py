from django.db import models
from django.shortcuts import reverse

class Department(models.Model):

    dept_name = models.CharField(max_length=50)
    budget = models.FloatField(max_length=50)

    class Meta:
        verbose_name = ("department")
        verbose_name_plural = ("departments")

    def __str__(self):
        return self.dept_name

    def get_absolute_url(self):
        return reverse("Department_detail", kwargs={"pk": self.pk})
