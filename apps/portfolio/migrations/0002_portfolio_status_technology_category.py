# Generated by Django 5.1.3 on 2024-11-21 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='portfolio',
            name='status',
            field=models.CharField(choices=[('draft', 'Draft'), ('published', 'Published'), ('archived', 'Archived')], default='draft', help_text='Current status of the portfolio item', max_length=20),
        ),
        migrations.AddField(
            model_name='technology',
            name='category',
            field=models.CharField(choices=[('frontend', 'Frontend'), ('backend', 'Backend'), ('database', 'Database'), ('devops', 'DevOps'), ('mobile', 'Mobile'), ('other', 'Other')], default='other', help_text='Category of the technology', max_length=20),
        ),
    ]
