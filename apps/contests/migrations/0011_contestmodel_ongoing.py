# Generated by Django 4.2.6 on 2023-10-22 20:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contests', '0010_alter_contestmodel_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='contestmodel',
            name='ongoing',
            field=models.BooleanField(default=True),
        ),
    ]