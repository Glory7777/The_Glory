# Generated by Django 4.2.3 on 2023-07-30 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('size', models.CharField(blank=True, max_length=256, null=True)),
                ('per', models.IntegerField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=256, null=True)),
                ('company', models.CharField(blank=True, max_length=256, null=True)),
                ('mtrl', models.CharField(blank=True, max_length=256, null=True)),
            ],
            options={
                'verbose_name': '전통주',
                'verbose_name_plural': '전통주들',
                'db_table': 'traditional_liq2',
            },
        ),
    ]