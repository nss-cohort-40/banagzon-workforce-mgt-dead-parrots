from django.db import models

class Training_program(models.Model):

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    max_attendees = models.IntegerField()

    class Meta:
        verbose_name = ("training_program")
        verbose_name_plural = ("training_programs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("training_program_detail", kwargs={"pk": self.pk})

