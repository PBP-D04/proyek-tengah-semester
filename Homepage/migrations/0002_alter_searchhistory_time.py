# Generated by Django 4.2.4 on 2023-12-01 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchhistory',
            name='time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]