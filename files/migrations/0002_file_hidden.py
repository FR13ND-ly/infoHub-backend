# Generated by Django 4.0.4 on 2022-05-15 10:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='hidden',
            field=models.BooleanField(default=False),
        ),
    ]
