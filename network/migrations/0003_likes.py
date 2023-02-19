# Generated by Django 4.0.6 on 2022-09-20 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_posts'),
    ]

    operations = [
        migrations.CreateModel(
            name='likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('liked_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='network.posts')),
            ],
        ),
    ]