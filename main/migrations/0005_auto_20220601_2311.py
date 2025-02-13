# Generated by Django 3.2.13 on 2022-06-01 14:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_notice'),
    ]

    operations = [
        migrations.AddField(
            model_name='notice',
            name='text',
            field=models.TextField(default='MODLE migration default value'),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.question')),
            ],
        ),
    ]
