from django.db import models

class EmployeeComputer(models.Model):
    """
    Creates the join table for the many to many relationship between computers and employees
    """

    employee = models.ForeignKey("Employee", on_delete=models.CASCADE)
    computer = models.ForeignKey("Computer", on_delete=models.CASCADE)
    assign_date = models.DateField(null=True, blank=True, default=None)
    unassign_date = models.DateField(null=True, blank=True, default=None)

