# Generated by Django 3.1.7 on 2021-12-14 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('instagram', '0006_auto_20211211_1904'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='instagram.task'),
        ),
    ]
