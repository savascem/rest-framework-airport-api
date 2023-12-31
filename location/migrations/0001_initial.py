# Generated by Django 4.2.6 on 2023-10-30 22:59

# Generated by Django 4.2.6 on 2023-10-30 19:49

from django.db import migrations, models
import django.db.models.deletion
import json
from django.utils.text import slugify


# country verilerini yükleyecek fonksiyon
def load_countries(apps, schema_editor):
    Country = apps.get_model('location', 'Country')
    with open('fixtures/countries.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            country = Country(
                name=item['name'],
                code=item['code'],
                phone_code=item['phone_code'],
                search_count=0,
            )
            country.save()


# city verilerini yükleyecek fonksiyon
def load_cities(apps, schema_editor):
    City = apps.get_model('location', 'City')
    Country = apps.get_model('location', 'Country')
    with open('fixtures/cities.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            country = Country.objects.get(code=item['country_code'])
            city = City(
                name=item['name'],
                country=country,
                search_count=0,
            )
            city.save()


# airport verilerini yükleyecek fonksiyon
def load_airports(apps, schema_editor):
    City = apps.get_model('location', 'City')
    Country = apps.get_model('location', 'Country')
    Airport = apps.get_model('location', 'Airport')
    with open('fixtures/cities.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for item in data:
            city = City.objects.get(name=item['name'], country__code=item['country_code'])
            country = Country.objects.get(code=item['country_code'])

            # airport verileri cities.json dosyası içinde airports key'i ile tanimlanmistir.
            # bu sebeple ikinci bir döngü yazma ihtiyaci duyulmus ve airport verilerine ulasilmistir.
            for aport in item['airports']:
                airport = Airport(
                    name=aport['name'],
                    code=aport['code'],
                    search_count=0,
                    city=city,
                    country=country,
                )
                airport.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('search_text', models.CharField(max_length=255)),
                ('search_count', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('phone_code', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('search_text', models.CharField(max_length=255)),
                ('search_count', models.IntegerField(default=0)),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.country')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Airport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('search_text', models.CharField(max_length=255)),
                ('search_count', models.IntegerField(default=0)),
                ('code', models.CharField(max_length=10, unique=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.city')),
                ('country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.country')),
            ],
            options={
                'abstract': False,
            },
        ),

        migrations.RunPython(load_countries),
        migrations.RunPython(load_cities),
        migrations.RunPython(load_airports),
    ]
