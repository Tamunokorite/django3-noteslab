# Generated by Django 3.2.5 on 2021-09-19 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_note_modified'),
    ]

    operations = [
        migrations.AddField(
            model_name='note',
            name='date_deleted',
            field=models.DateTimeField(null=True),
        ),
    ]