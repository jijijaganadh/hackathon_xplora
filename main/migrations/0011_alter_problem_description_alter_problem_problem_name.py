# Generated by Django 4.1.3 on 2023-01-12 04:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_mainparticipant_institution_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='description',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='problem',
            name='problem_name',
            field=models.CharField(max_length=100),
        ),
    ]
