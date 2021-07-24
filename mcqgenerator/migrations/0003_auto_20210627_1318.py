# Generated by Django 3.1.3 on 2021-06-27 12:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mcqgenerator', '0002_lecturemodel_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='hello world', max_length=50)),
                ('date', models.DateField(auto_now_add=True)),
                ('slug', models.SlugField(null=True)),
                ('lecture', models.FileField(upload_to='lectures')),
            ],
        ),
        migrations.DeleteModel(
            name='LectureModel',
        ),
    ]
