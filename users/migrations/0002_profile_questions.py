# Generated by Django 3.2.4 on 2021-07-14 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqgenerator', '0013_auto_20210702_1937'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='questions',
            field=models.ManyToManyField(to='mcqgenerator.Question'),
        ),
    ]
