# Generated by Django 3.1.7 on 2021-12-10 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0003_chunk_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='action_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
