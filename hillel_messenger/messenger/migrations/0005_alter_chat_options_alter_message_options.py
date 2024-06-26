# Generated by Django 5.0.6 on 2024-05-30 07:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('messenger', '0004_alter_chat_options_alter_message_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='chat',
            options={'permissions': [('can_create_chat', 'Can Create chat'), ('can_add_users_to_chat', 'Can Add users to chat'), ('can_remove_users_from_chat', 'Can Remove users from chat')]},
        ),
        migrations.AlterModelOptions(
            name='message',
            options={'permissions': [('can_edit_own_message', 'Can Edit own message'), ('can_delete_own_message', 'Can Delete own message')]},
        ),
    ]
