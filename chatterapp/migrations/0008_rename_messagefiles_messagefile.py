# Generated by Django 4.1.1 on 2022-11-24 19:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chatterapp', '0007_alter_room_private_messagefiles'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MessageFiles',
            new_name='MessageFile',
        ),
    ]