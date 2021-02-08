from django.db import models
from datetime import date,datetime

class Departments(models.Model):
    department_name = models.CharField(max_length=150, verbose_name="Departman Adı:")
    department_mail = models.CharField(max_length=150, verbose_name="Departman Mail:")

    def __str__(self):
        return str(self.department_name)


class PBI(models.Model):
    department = models.ForeignKey(Departments, on_delete=models.CASCADE, verbose_name="Department",
                                   related_name="department",default='')
    # department_name = models.CharField(max_length=100, verbose_name="Departmant")
    sprint = models.CharField(max_length=100, verbose_name="Sprint",default=str(datetime.now().month) +"/"+str(datetime.now().year))
    end_day_index = models.CharField(max_length=100, verbose_name="İş Günü Sayısı")
    pbi_type = models.CharField(max_length=100, verbose_name="Type")
    pbi = models.CharField(max_length=200, verbose_name="PBI")
    classficition = models.CharField(max_length=100, verbose_name="Classification")
    workorder_date = models.DateField(verbose_name="Workorder Date", null=True, blank=True)
    start_date = models.DateField(verbose_name="Start Date", null=True, blank=True)
    finish_date = models.DateField(verbose_name="Finish Date", null=True, blank=True)
    actual_date = models.DateField(verbose_name="Actual Date", null=True, blank=True)






