from django.db import models
from datetime import datetime, date
from django.contrib.auth.models import User


class TabRecord(models.Model):
    company_name = models.CharField(max_length=255)
    date = models.DateField()
    revenue = models.DecimalField(max_digits=15, decimal_places=2)
    expenses = models.DecimalField(max_digits=15, decimal_places=2)
    profit = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.profit = self.revenue - self.expenses
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.company_name} ({self.date})"
    
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Добавляем связь с пользователем
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    position = models.CharField(max_length=100, verbose_name="Должность")
    date_joined = models.DateField(verbose_name="Дата приема на работу")

    def __str__(self):
        return f"{self.last_name} {self.first_name}"

class Tabel(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.TimeField(null=True, blank=True)
    time_out = models.TimeField(null=True, blank=True)
    hours = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.time_in and self.time_out:
            delta = datetime.combine(date.min, self.time_out) - datetime.combine(date.min, self.time_in)
            self.hours = round(delta.total_seconds() / 3600, 2)
        super().save(*args, **kwargs)
