# Generated by Django 4.2.2 on 2023-06-23 08:27

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("musker", "0003_alter_profile_date_modified_meep"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="profile_image",
            field=models.ImageField(blank=True, null=True, upload_to="images/"),
        ),
    ]
