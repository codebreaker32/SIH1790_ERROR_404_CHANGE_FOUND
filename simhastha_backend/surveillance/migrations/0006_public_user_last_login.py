# Generated by Django 5.1.1 on 2024-09-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('surveillance', '0005_alter_report_status_staffuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='public_user',
            name='last_login',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
