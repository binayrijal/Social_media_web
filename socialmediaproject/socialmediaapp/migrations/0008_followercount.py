# Generated by Django 4.1.3 on 2024-02-13 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('socialmediaapp', '0007_like'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowerCount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('follower', models.CharField(max_length=100)),
                ('user', models.CharField(max_length=100)),
            ],
        ),
    ]
