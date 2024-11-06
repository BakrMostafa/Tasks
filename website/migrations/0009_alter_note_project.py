# Generated by Django 4.2.13 on 2024-11-06 11:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0008_alter_note_project'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='project',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_notes', to='website.project'),
        ),
    ]
