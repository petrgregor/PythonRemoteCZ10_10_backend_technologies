# Generated by Django 4.1.1 on 2022-11-24 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatterapp', '0008_rename_messagefiles_messagefile'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='file',
            field=models.TextField(null=True),
        ),
    ]
