# Generated by Django 4.2.4 on 2023-11-29 04:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Homepage', '0002_searchhistory'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('DetailBook', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentV2',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_book', to='Homepage.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_comment', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]