# Generated by Django 4.2.5 on 2023-09-30 01:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Video', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='video',
            name='title',
        ),
    ]
