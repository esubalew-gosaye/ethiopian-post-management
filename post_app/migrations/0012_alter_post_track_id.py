# Generated by Django 4.0.2 on 2022-03-19 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0011_alter_post_track_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='track_id',
            field=models.CharField(blank=True, default='f19DE', max_length=10),
        ),
    ]
