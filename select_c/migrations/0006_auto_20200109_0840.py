# Generated by Django 3.0.2 on 2020-01-09 08:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('select_c', '0005_auto_20200109_0838'),
    ]

    operations = [
        migrations.AddField(
            model_name='e',
            name='kscj',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='e',
            name='pscj',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='e',
            name='zpcj',
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name='o',
            name='credit',
            field=models.IntegerField(default=0),
        ),
    ]