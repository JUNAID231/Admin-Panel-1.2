# Generated by Django 2.1.7 on 2019-04-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('troyapi', '0003_chat'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChatUser',
            fields=[
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('emailaddress', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('token', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('picture', models.ImageField(default='profile_image/default.jpg', max_length=255, upload_to='profile_image')),
            ],
        ),
    ]
