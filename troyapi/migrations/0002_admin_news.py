# Generated by Django 2.1.7 on 2019-04-01 14:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troyapi', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('emailaddress', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('admin_id', models.AutoField(primary_key=True, serialize=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('suspend', models.CharField(default='False', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('category', models.CharField(max_length=100)),
                ('title', models.CharField(max_length=150)),
                ('short_description', models.CharField(max_length=200)),
                ('long_description', models.TextField()),
                ('photo', models.ImageField(default='default.png', upload_to='profile_image')),
                ('auther', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('news_id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
    ]