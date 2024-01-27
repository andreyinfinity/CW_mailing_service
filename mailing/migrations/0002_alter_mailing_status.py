# Generated by Django 4.2.7 on 2024-01-05 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mailing',
            name='status',
            field=models.CharField(choices=[('created', 'created'), ('in progress', 'in progress'), ('sending', 'sending'), ('stopped', 'stopped'), ('completed', 'completed')], default='created', max_length=50, verbose_name='статус'),
        ),
    ]
