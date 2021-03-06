# Generated by Django 2.2.2 on 2019-06-16 21:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Port',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=5)),
                ('name', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('slug', models.SlugField()),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='rates_api.Region')),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField(choices=[(1, 'Monday'), (2, 'Tuesday'), (3, 'Wednesday'), (4, 'Thursday'), (5, 'Friday'), (6, 'Saturday'), (7, 'Sunday')])),
                ('price', models.DecimalField(decimal_places=2, max_digits=20)),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_destination', to='rates_api.Port')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price_origin', to='rates_api.Port')),
            ],
        ),
        migrations.AddField(
            model_name='port',
            name='region',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rates_api.Region'),
        ),
    ]
