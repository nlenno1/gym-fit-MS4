# Generated by Django 4.0.2 on 2022-03-09 13:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("instructors", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="instructor",
            name="description",
            field=models.TextField(blank=True, max_length=255, null=True),
        ),
    ]
