# Generated by Django 2.2.4 on 2019-08-20 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sendmail', '0002_auto_20190820_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='attachments/'),
        ),
    ]
