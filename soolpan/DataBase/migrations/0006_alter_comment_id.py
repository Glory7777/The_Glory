# Generated by Django 4.2.4 on 2023-08-08 06:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DataBase', '0005_comment_carbon_comment_color_comment_flavor_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]