# Generated by Django 3.0.2 on 2020-01-14 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vendor', '0002_auto_20200114_0523'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vendoruser',
            options={'verbose_name': 'Vendor User', 'verbose_name_plural': 'Users'},
        ),
    ]
