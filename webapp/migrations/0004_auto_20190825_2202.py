# Generated by Django 2.2.4 on 2019-08-25 19:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20190825_2134'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quote_log',
            name='error_code',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='quote_log',
            name='message',
            field=models.TextField(default='No error'),
        ),
    ]
