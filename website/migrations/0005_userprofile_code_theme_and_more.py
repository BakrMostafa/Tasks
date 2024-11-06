# Generated by Django 4.2.13 on 2024-11-06 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_task_completion_date_task_start_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='code_theme',
            field=models.CharField(choices=[('github', 'GitHub'), ('monokai', 'Monokai'), ('dracula', 'Dracula'), ('solarized', 'Solarized')], default='github', max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='desktop_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='email_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='github_access_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='gitlab_access_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='jira_access_token',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='mention_notifications',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='sidebar_collapsed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='theme',
            field=models.CharField(choices=[('light', 'Light'), ('dark', 'Dark'), ('system', 'System Default')], default='system', max_length=10),
        ),
    ]
