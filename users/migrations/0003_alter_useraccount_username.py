# Generated by Django 4.0.1 on 2022-04-04 22:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_useraccount_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccount',
            name='username',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='Username'),
        ),
    ]
