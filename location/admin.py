from django.contrib import admin
from .models import Country, City, Airport

# disp_list ile admin panelde gorunur olmasi istenen sutunlar tanimlandi.
disp_list = [
        'name', 'search_text', 'search_count'
    ]


class CountryAdmin(admin.ModelAdmin):
    list_display = disp_list


class CityAdmin(admin.ModelAdmin):
    list_display = disp_list


class AirportAdmin(admin.ModelAdmin):
    list_display = disp_list


# country, city ve airport alanlarinin Admin panele eklendi
admin.site.register(Country, CountryAdmin)
admin.site.register(City, CityAdmin)
admin.site.register(Airport, AirportAdmin)
