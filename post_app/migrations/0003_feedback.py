# Generated by Django 4.0.2 on 2022-03-01 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post_app', '0002_alter_config_cost_alter_config_distance'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=21)),
                ('email', models.EmailField(max_length=254)),
                ('subject', models.CharField(blank=True, max_length=30, null=True)),
                ('body', models.TextField(max_length=200)),
            ],
        ),
    ]
