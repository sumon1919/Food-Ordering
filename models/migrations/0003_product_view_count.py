# Generated by Django 4.2.5 on 2023-11-11 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('models', '0002_product_user_alter_product_imgs'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='view_count',
            field=models.IntegerField(default=1),
        ),
    ]
