# Generated by Django 5.1.1 on 2024-10-13 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0012_alter_review_user_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='Instructor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='isntructor')),
                ('name', models.CharField(max_length=244)),
                ('designation', models.CharField(max_length=355)),
            ],
        ),
    ]
