# Generated by Django 3.1.4 on 2021-01-22 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0015_auto_20210122_1753'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pbi',
            name='actual_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Actual Date'),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='finish_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Finish Date'),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='sprint',
            field=models.CharField(max_length=100, verbose_name='Sprint'),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='start_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Start Date'),
        ),
        migrations.AlterField(
            model_name='pbi',
            name='workorder_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Workorder Date'),
        ),
    ]
