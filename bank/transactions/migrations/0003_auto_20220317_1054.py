# Generated by Django 3.2.12 on 2022-03-17 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('transactions', '0002_auto_20220317_1019'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='new_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18),
        ),
        migrations.AddField(
            model_name='transaction',
            name='old_balance',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=18),
        ),
    ]