# Generated by Django 3.2 on 2023-03-28 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_remove_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password',
            field=models.CharField(default='dasha', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
    ]