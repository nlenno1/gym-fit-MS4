# Generated by Django 4.0.2 on 2022-03-05 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0006_rename_date_singleexerciseclass_class_date_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classcategory',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
        migrations.AlterField(
            model_name='singleexerciseclass',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
