# Generated by Django 2.0.7 on 2018-07-09 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ChatServer', '0003_auto_20180709_1300'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='Birthday',
            field=models.CharField(max_length=24),
        ),
    ]