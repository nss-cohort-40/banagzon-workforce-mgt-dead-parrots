from django.db import models

class Employee_training_program(models.Model):

    """
    Creates the join table for the many to many relationship between training programs and employees
    Author: Ronald Lankford
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    training_program = models.ForeignKey("Training_program", on_delete=models.CASCADE)

    class Meta:
        verbose_name = ("employee_training_program")
        verbose_name_plural = ("employee_training_programs")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("employee_training_program_detail", kwargs={"pk": self.pk})
