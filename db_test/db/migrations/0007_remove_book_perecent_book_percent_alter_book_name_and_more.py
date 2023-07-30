# Generated by Django 4.2.3 on 2023-07-30 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0006_alter_book_company_alter_book_mtrl_alter_book_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='perecent',
        ),
        migrations.AddField(
            model_name='book',
            name='percent',
            field=models.IntegerField(blank=True, null=True, verbose_name='perecnt'),
        ),
        migrations.AlterField(
            model_name='book',
            name='name',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='name'),
        ),
        migrations.AlterField(
            model_name='book',
            name='size',
            field=models.CharField(blank=True, max_length=256, null=True, verbose_name='size'),
        ),
    ]
