# Generated by Django 4.2.7 on 2023-12-08 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0006_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='adress',
            field=models.CharField(blank=True, max_length=150),
        ),
    ]
