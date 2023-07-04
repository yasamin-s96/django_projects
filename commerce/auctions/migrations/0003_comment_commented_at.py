# Generated by Django 4.2.1 on 2023-07-04 05:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("auctions", "0002_remove_comment_commented_at"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="commented_at",
            field=models.DateTimeField(
                auto_now_add=True, default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
    ]
