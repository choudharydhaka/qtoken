# Generated by Django 3.0.6 on 2020-05-08 22:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('created_date', models.DateTimeField(verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='LiquorStore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('is_active', models.BooleanField()),
                ('token_date', models.DateTimeField(verbose_name='date Token')),
            ],
        ),
        migrations.CreateModel(
            name='StoreOwnmer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mobile_number', models.CharField(max_length=200)),
                ('name', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Token',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token_number', models.CharField(max_length=1000)),
                ('token_valid', models.BooleanField()),
                ('token_date', models.DateTimeField(verbose_name='date Token')),
                ('consumer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquor.Consumer')),
                ('store', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquor.LiquorStore')),
            ],
        ),
        migrations.AddField(
            model_name='liquorstore',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='liquor.StoreOwnmer'),
        ),
    ]
