# Generated by Django 4.2.6 on 2023-11-02 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, default=None, max_length=20, unique=True),
        ),
    ]
