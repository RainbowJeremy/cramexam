# Generated by Django 3.1.3 on 2021-06-25 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqgenerator', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecturemodel',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
