# Generated by Django 4.2.6 on 2023-10-28 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bookphoria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='thumbnail',
            field=models.URLField(blank=True, null=True),
        ),
    ]