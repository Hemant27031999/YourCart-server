# Generated by Django 2.2.1 on 2019-09-18 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base_tech', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hotel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('hotel_Main_Img', models.ImageField(upload_to='images/')),
            ],
        ),
    ]