# Generated by Django 4.1.2 on 2022-10-22 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sub', '0002_alter_subscription_team_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subscription',
            name='team_name',
            field=models.CharField(max_length=100, verbose_name='Назва команди'),
        ),
    ]
