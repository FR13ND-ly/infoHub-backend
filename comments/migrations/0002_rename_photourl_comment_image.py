# Generated by Django 3.2.3 on 2022-06-17 11:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='photoUrl',
            new_name='image',
        ),
    ]
