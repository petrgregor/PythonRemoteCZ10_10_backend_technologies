# Generated by Django 4.1.1 on 2022-11-23 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatterapp', '0003_alter_room_private'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='private',
            field=models.BooleanField(),
        ),
    ]
