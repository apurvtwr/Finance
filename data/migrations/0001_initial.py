# Generated by Django 3.0.7 on 2020-06-10 01:09

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ticker', models.TextField(unique=True)),
                ('name', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
