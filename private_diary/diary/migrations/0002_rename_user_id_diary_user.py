# Generated by Django 3.2.19 on 2023-08-24 08:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('diary', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='diary',
            old_name='user_id',
            new_name='user',
        ),
    ]
