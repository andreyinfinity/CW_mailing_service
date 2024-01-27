# Generated by Django 4.2.7 on 2024-01-27 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mailing', '0005_remove_logs_mailing_remove_logs_user_logs_mailing_pk_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='logs',
            name='mailing_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='название рассылки'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='mailing_pk',
            field=models.IntegerField(verbose_name='id рассылки'),
        ),
        migrations.AlterField(
            model_name='logs',
            name='user_pk',
            field=models.IntegerField(verbose_name='id пользователя'),
        ),
    ]
