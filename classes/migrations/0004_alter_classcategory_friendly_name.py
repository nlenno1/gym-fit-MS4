# Generated by Django 4.0.2 on 2022-03-14 19:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0003_alter_classcategory_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classcategory',
            name='friendly_name',
            field=models.CharField(default='Default Class Category Name', max_length=254),
            preserve_default=False,
        ),
    ]
