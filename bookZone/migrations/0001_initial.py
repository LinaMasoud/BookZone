# Generated by Django 2.0.2 on 2018-02-23 13:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('country', models.CharField(max_length=50)),
                ('bio', models.TextField()),
                ('born_at', models.DateField(verbose_name='Born At')),
                ('died_at', models.DateField(verbose_name='Died At')),
                ('author_pic', models.ImageField(default='/home/linamasoud/Documents/user.png', upload_to='')),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desciption', models.TextField()),
                ('published_at', models.DateField(verbose_name='date published')),
                ('book_pic', models.ImageField(default='/home/linamasoud/Documents/book.png', upload_to='')),
                ('author_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookZone.Author')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('desciption', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='rateBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rate', models.IntegerField(default=0)),
                ('book_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bookZone.Book')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='book',
            name='categories',
            field=models.ManyToManyField(to='bookZone.Category'),
        ),
        migrations.AddField(
            model_name='book',
            name='users_read',
            field=models.ManyToManyField(related_name='User_Book_read', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='book',
            name='users_wishlist',
            field=models.ManyToManyField(related_name='User_Book_Wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]
