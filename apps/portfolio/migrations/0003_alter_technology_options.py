# Generated by Django 5.1.3 on 2024-11-14 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0002_alter_portfolioimage_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='technology',
            options={'ordering': ['name', '-created_at'], 'verbose_name_plural': 'Technologies'},
        ),
    ]
