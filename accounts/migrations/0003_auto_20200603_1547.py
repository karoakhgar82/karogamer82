# Generated by Django 3.0.6 on 2020-06-03 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_remove_userpro_discription'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpro',
            name='username',
            field=models.CharField(max_length=100, verbose_name='What song are you going to sing?'),
        ),
    ]
