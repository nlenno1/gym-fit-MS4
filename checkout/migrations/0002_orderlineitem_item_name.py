# Generated by Django 4.0.2 on 2022-03-13 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderlineitem',
            name='item_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
