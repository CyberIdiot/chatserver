# Generated by Django 2.0.7 on 2018-07-08 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Messages',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('MessageType', models.CharField(max_length=10)),
                ('MessageDate', models.DateTimeField()),
                ('MessageCont', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NickName', models.CharField(max_length=32)),
                ('Birthday', models.DateField()),
                ('Friends', models.ManyToManyField(related_name='_userprofile_Friends_+', to='ChatServer.UserProfile')),
                ('LinkUser', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='messages',
            name='MessageFrom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MessageFrom', to='ChatServer.UserProfile'),
        ),
        migrations.AddField(
            model_name='messages',
            name='MessageTo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='MessageTo', to='ChatServer.UserProfile'),
        ),
    ]
