# Generated by Django 4.0.2 on 2022-03-21 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_last_name_revoke'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revoke',
            name='code',
            field=models.CharField(blank=True, default='POST:ZJFCY', max_length=15),
        ),
    ]