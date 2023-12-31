# Generated by Django 4.2.7 on 2023-12-19 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0002_alter_mailing_mail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='create_date',
            field=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'),
        ),
        migrations.AlterField(
            model_name='mailing',
            name='send_date',
            field=models.DateTimeField(default=models.DateTimeField(auto_now_add=True, verbose_name='дата создания'), verbose_name='дата отправления'),
        ),
    ]