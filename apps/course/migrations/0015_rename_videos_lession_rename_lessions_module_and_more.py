# Generated by Django 5.1.1 on 2024-10-14 07:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0014_course_instructor_assingment_projects'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Videos',
            new_name='Lession',
        ),
        migrations.RenameModel(
            old_name='Lessions',
            new_name='Module',
        ),
        migrations.RenameField(
            model_name='lession',
            old_name='lession',
            new_name='module',
        ),
    ]
