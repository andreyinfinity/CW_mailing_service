# Generated by Django 4.2.7 on 2023-12-18 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='first_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Имя'),
        ),
    ]