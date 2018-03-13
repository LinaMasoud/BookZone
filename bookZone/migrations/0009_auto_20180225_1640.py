# Generated by Django 2.0.2 on 2018-02-25 16:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bookZone', '0008_auto_20180224_1640'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='cat_pic',
            field=models.ImageField(default='/home/linamasoud/Documents/user.png', upload_to='bookZone/static/images/categories'),
        ),
        migrations.AlterField(
            model_name='author',
            name='users',
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]
