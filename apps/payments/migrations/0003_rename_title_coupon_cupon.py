# Generated by Django 5.1.1 on 2024-10-16 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_coupon_parcentige'),
    ]

    operations = [
        migrations.RenameField(
            model_name='coupon',
            old_name='title',
            new_name='cupon',
        ),
    ]
