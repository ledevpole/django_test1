# Generated by Django 3.1 on 2020-08-10 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_wiki', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_content',
            field=models.TextField(),
        ),
    ]
