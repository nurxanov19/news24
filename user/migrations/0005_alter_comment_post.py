# Generated by Django 5.1.7 on 2025-04-02 08:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_contact'),
        ('user', '0004_comment_edited_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='news.news'),
        ),
    ]
