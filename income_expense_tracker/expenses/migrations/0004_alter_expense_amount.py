# Generated by Django 3.2.5 on 2021-07-27 10:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0003_alter_expense_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='expense',
            name='amount',
            field=models.PositiveIntegerField(),
        ),
    ]
