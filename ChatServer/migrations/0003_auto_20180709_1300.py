# Generated by Django 2.0.7 on 2018-07-09 05:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatServer', '0002_auto_20180709_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appuser',
            name='Email',
            field=models.EmailField(blank=True, max_length=254),
        ),
        migrations.AlterField(
            model_name='appuser',
            name='UserName',
            field=models.CharField(max_length=150, unique=True),
        ),
    ]