# Generated by Django 4.1.3 on 2023-03-17 05:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_rename_follower_id_user_followers_follower_email_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User_posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100)),
                ('post', models.JSONField()),
            ],
        ),
    ]
