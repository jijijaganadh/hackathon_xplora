# Generated by Django 4.1.3 on 2023-01-16 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_mainparticipant_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='mainparticipant',
            name='remark',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='mainparticipant',
            name='status',
            field=models.CharField(max_length=1),
        ),
    ]
