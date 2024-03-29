# Generated by Django 3.1.2 on 2020-11-17 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training_planner', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='exercise',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='rangeunit',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='trainingsquery',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
        migrations.AlterField(
            model_name='valueunit',
            name='description',
            field=models.CharField(blank=True, max_length=2000),
        ),
    ]
