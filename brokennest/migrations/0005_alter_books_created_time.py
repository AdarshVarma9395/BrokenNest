# Generated by Django 5.0.1 on 2024-01-24 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("brokennest", "0004_alter_books_created_time"),
    ]

    operations = [
        migrations.AlterField(
            model_name="books",
            name="created_time",
            field=models.DateTimeField(null=True),
        ),
    ]