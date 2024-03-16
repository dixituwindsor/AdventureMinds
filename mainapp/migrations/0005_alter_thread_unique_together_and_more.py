# Generated by Django 5.0.2 on 2024-03-14 19:30

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("mainapp", "0004_remove_message_recipient_remove_message_sender_and_more"),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name="thread",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="thread",
            name="first_person",
        ),
        migrations.RemoveField(
            model_name="thread",
            name="second_person",
        ),
        migrations.DeleteModel(
            name="ChatMessage",
        ),
        migrations.DeleteModel(
            name="Thread",
        ),
    ]
