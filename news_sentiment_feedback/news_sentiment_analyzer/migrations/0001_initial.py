# Generated by Django 4.2.11 on 2024-03-09 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('video_id', models.CharField(max_length=20, unique=True)),
                ('description', models.TextField()),
            ],
        ),
    ]