# Generated by Django 3.2.3 on 2022-05-09 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_auto_20220509_1746'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='coverImage',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='coverImageDescription',
            field=models.TextField(default=''),
        ),
    ]
