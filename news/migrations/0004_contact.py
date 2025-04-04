# Generated by Django 5.1.7 on 2025-03-25 05:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_alter_news_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('message', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('views', models.PositiveIntegerField(default=0)),
            ],
        ),
    ]
