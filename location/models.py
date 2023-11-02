from django.db import models
from django.db.models import Q


class LocationQuerySet(models.QuerySet):
    def search(self, query=None):
        if not query or query.strip() == "":
            return self.none()

        # query = unidecode(query)
        query = query.lower()

        # veri tabani kayitlarinda unaccent search yapacilmek icin postgres veri tabaninda 
        # CREATE EXTENSION unaccent; komutu calistirilmali
        lookups = Q(search_text__unaccent__icontains=query)
        return self.filter(lookups)


# Arama islemlerini yonetmek icin Manager miras alan bir class tanımlandı
class LocationManager(models.Manager):
    def get_queryset(self):
        return LocationQuerySet(self.model, using=self._db)
    
    def search(self, query=None):
        return self.get_queryset().search(query=query)


# Country, City ve Airport sınıflarının ortak alanlarını içeren bir abstract sınıf tanımlandı
# name, search_text, search_count alanlari zorunludur
class RootModel(models.Model):
    name = models.CharField(max_length=255, blank=False)
    search_text = models.CharField(max_length=255, blank=False)
    search_count = models.IntegerField(default=0)


    class Meta:
        abstract = True


# country alani RootModel sinifinin ozelliklerini alir 
# code degeri doldurulmasi ve unique olmasi zorunlu tutlmustur
class Country(RootModel):
    code = models.CharField(max_length=10, unique=True, blank=False)
    phone_code = models.CharField(max_length=20)

    objects = LocationManager()

    def __str__(self):
        return self.code


# city alani RootModel sinifi ozelliklerini alir
# Bir ulke icerisinde ayni isimde sehirler olabilecegi icin uniqe degeri yoktur.
class City(RootModel):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    objects = LocationManager()

    def __str__(self):
        return self.name


# airport alani RootModel sinifi ozelliklerini alir
# airport code bos birakilamaz ve unique olmalidir.
class Airport(RootModel):
    code = models.CharField(max_length=10, unique=True, blank=False)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    objects = LocationManager()

    def __str__(self):
        return self.code