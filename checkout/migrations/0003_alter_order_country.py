# Generated by Django 3.2.13 on 2022-07-04 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('checkout', '0002_auto_20220630_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='country',
            field=models.CharField(default='GB', max_length=30),
        ),
    ]
