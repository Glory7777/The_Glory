# Generated by Django 4.2.4 on 2023-08-12 05:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0010_alter_tal_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tal',
            name='like',
            field=models.IntegerField(blank=True, default=0, verbose_name='전체 like Count'),
        ),
    ]
