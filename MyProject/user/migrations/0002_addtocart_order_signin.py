# Generated by Django 3.2.2 on 2021-10-02 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='addtocart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('userid', models.EmailField(max_length=100)),
                ('status', models.BooleanField()),
                ('cdate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pid', models.IntegerField()),
                ('userid', models.EmailField(max_length=100)),
                ('remarks', models.CharField(max_length=40)),
                ('status', models.BooleanField()),
                ('odate', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='signin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('passwd', models.CharField(max_length=120)),
            ],
        ),
    ]