# Generated by Django 3.1.3 on 2021-06-16 08:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='city',
            field=models.CharField(blank=True, default='Not specified', max_length=10),
        ),
    ]
