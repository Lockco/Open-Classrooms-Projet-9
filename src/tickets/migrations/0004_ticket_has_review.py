# Generated by Django 4.1.5 on 2023-02-17 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tickets", "0003_remove_ticket_public_responses"),
    ]

    operations = [
        migrations.AddField(
            model_name="ticket",
            name="has_review",
            field=models.BooleanField(default=False),
        ),
    ]
