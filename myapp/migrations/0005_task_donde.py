# Generated by Django 5.2 on 2025-05-20 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_rename_tasks_task'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='donde',
            field=models.BooleanField(default=False),
        ),
    ]
