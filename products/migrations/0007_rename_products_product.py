# Generated by Django 3.2.13 on 2022-06-02 13:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_auto_20220602_1317'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]