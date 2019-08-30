# Generated by Django 2.2.3 on 2019-07-20 15:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0007_auto_20190720_1214'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='rank',
        ),
        migrations.RemoveField(
            model_name='post',
            name='state',
        ),
        migrations.AddField(
            model_name='post',
            name='rate',
            field=models.SmallIntegerField(db_index=True, default=1, verbose_name='文章进度(1-5,计划中，草稿，编写中，待完善，已完成)'),
        ),
    ]
