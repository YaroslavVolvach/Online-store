# Generated by Django 3.1.3 on 2021-08-14 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_auto_20210814_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='gender',
            field=models.CharField(choices=[('N', 'Not specified'), ('F', 'Female'), ('M', 'Male')], default='Not specified', max_length=13),
        ),
    ]
