# Generated by Django 3.2.4 on 2021-06-29 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqgenerator', '0010_auto_20210629_1244'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
