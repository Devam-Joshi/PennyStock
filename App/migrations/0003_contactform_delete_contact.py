# Generated by Django 4.0.3 on 2022-03-30 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0002_alter_contact_msg'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contactform',
            fields=[
                ('sno', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('email', models.CharField(max_length=150)),
                ('message', models.CharField(max_length=255)),
            ],
        ),
        migrations.DeleteModel(
            name='Contact',
        ),
    ]