# Generated by Django 4.1.4 on 2023-01-26 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("course", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="semester",
            name="syllabus",
            field=models.FileField(blank=True, upload_to="media/syllabus"),
        ),
    ]
