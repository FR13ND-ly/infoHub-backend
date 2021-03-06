# Generated by Django 4.0.4 on 2022-06-07 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=200)),
                ('link', models.CharField(max_length=200)),
                ('image', models.CharField(max_length=200)),
                ('author', models.CharField(max_length=200)),
                ('activated', models.BooleanField(default=False)),
            ],
        ),
    ]
