# Generated by Django 5.1.3 on 2024-11-14 06:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='portfolioimage',
            options={'ordering': ['order', '-created_at']},
        ),
    ]