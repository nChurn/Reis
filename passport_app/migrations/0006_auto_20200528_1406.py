# Generated by Django 2.2.5 on 2020-05-28 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('passport_app', '0005_rateclassifier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='point',
            field=models.CharField(default='', max_length=20, null=True),
        ),
    ]
