# Generated by Django 4.2.6 on 2023-11-02 22:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('analysis', '0004_taskmetadata_enable_internet'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskmetadata',
            name='machine',
            field=models.CharField(default='auto', max_length=22),
        ),
    ]