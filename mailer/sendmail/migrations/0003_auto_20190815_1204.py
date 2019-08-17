# Generated by Django 2.2.4 on 2019-08-15 12:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0002_auto_20190815_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='bcc',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='email',
            name='cc',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), blank=True, default=list, size=None),
        ),
        migrations.AlterField(
            model_name='email',
            name='to',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.EmailField(max_length=254), default=list, size=None),
        ),
    ]