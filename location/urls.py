from django.urls import path
from . import views

urlpatterns = [
    ### ORTAK GOREVLER ###
    # search api endpointleri
    # ornek url adresi ---> http://127.0.0.1:8000/api/search/city/?query=ESKİŞehİr
    path('search/country/', views.CountrySearchAPI.as_view(), name='country-search'),
    path('search/city/', views.CitiesSearchAPI.as_view(), name='city-search'),
    path('search/airport/', views.AirportsSearchAPI.as_view(), name='airport-search'),

    # selection api endpointleri
    # ornek url adresi ---> http://127.0.0.1:8000/api/select/airport/15 
    path('select/airport/<int:pk>/', views.AirportsSelectView.as_view(), name='select_airport'),
    path('select/city/<int:pk>/', views.CitiesSelectView.as_view(), name='select_city'),
    path('select/country/<int:pk>/', views.CountriesSelectView.as_view(), name='select_country'),

    # deselect api endpoint
    # ornek url adresi ---> http://127.0.0.1:8000/api/deselect/
    path('deselect/', views.DeselectLocationView.as_view(), name='deselect'),

    ### GOREVLER ###
    # ulke koduna gore en cok aranan bes sehrin listelendigi api endpoint
    # ornek url adresi ---> http://127.0.0.1:8000/api/country-most-searched-cities/?country_code=US&country_code=CN
    path('country-most-searched-cities/', views.CountryMostSearchedCitiesAPI.as_view(), name='country-most-searched-cities'),

    # ulke koduna gore toplam sehir arama sayisi/airport arama sayisinin listelendigi api endpoint
    # ornek url adresi ---> http://127.0.0.1:8000/api/country-searched-ratio/?country_code=US&country_code=CN
    path('country-searched-ratio/', views.CountrySearchRatioAPI.as_view(), name='country-searched-ratio'),
]