from .models import Airport, City, Country
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CountrySerializer, CitySerializer, AirportSerializer
from django.db.models import Sum

####################### ORTAK GOREVLER BASLANGIC #######################

#######################
# Search API endpointleri bu alanda tanimlanmistir.

# LocationSearch class parent class olarak tanimlanmistir. 
# Location appinde ki modeller search islemi icin bu class'i miras olarak almistir
class LocationSearch(APIView):
    def search(self, request, query, model, model_title):
        if query:
            data = model.objects.search(query)

            data = data[0:20]

            if model_title == 'country':
                results = {
                    'countries': [{'name': country.name, 'code': country.code} for country in data],
                }

                return Response(results)

            elif model_title == 'city':
                results = {
                    'cities': [{'name': city.name, 'country': city.country.name} for city in data],
                }

                return Response(results)

            elif model_title == 'airport':
                results = {
                    'airports': [{'name':airport.name, 'city': airport.city.name, 'country': airport.city.country.name} for airport in data],
                }
                
                return Response(results)
            
            return Response('Aranan kriterlere uygun kayit bulunamadi.')

        return Response({'error': 'Arama sorgusu eksik.'})
    

# country-search api endpointi icin olusturulmus classtir
class CountrySearchAPI(LocationSearch):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        return self.search(request, query=query, model=Country, model_title='country')


# city-search api endpointi icin olusturulmus classtir
class CitiesSearchAPI(LocationSearch):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        return self.search(request, query=query, model=City, model_title='city')
    

# airport-search api endpointi icin olusturulmus classtir
class AirportsSearchAPI(LocationSearch):
    def get(self, request, *args, **kwargs):
        query = request.query_params.get('query')
        return self.search(request, query=query, model=Airport, model_title='airport')
    

#######################
# Selection API endpointleri bu alanda tanimlanmistir.

# LocationSelectViewBase classı parent class olarak tanimlanmistir. 
# Location appinde ki modeller, selection islemi icin bu class'i miras olarak almistir
class LocationSelectViewBase(generics.RetrieveUpdateDestroyAPIView):
    def select_location(self, request, instance_type):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Oturum bilgileri
        request.session['selected_location'] = f'{instance_type}_{instance.id}'
        # Oturumu kaydetme
        request.session.save()
        instance.search_count += 1
        if instance_type == 'Country':
            instance.save()
        elif instance_type == 'City':
            instance.save()
            instance.country.search_count += 1
            instance.country.save()
        else:
            instance.save()
            instance.country.search_count += 1
            instance.country.save()
            instance.city.search_count += 1
            instance.city.save()
        
        return Response(serializer.data)


# select_airport api endpointi icin olusturulmus classtir
class AirportsSelectView(LocationSelectViewBase):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    
    def get(self, request, *args, **kwargs):
        return self.select_location(request, 'Airport')

    def delete(self, request, *args, **kwargs):
        return self.deselect_location(request)


# select_city api endpointi icin olusturulmus classtir
class CitiesSelectView(LocationSelectViewBase):
    queryset = City.objects.all()
    serializer_class = CitySerializer
    
    def get(self, request, *args, **kwargs):
        return self.select_location(request, 'City')

    def delete(self, request, *args, **kwargs):
        return self.deselect_location(request)


# select_country api endpointi icin olusturulmus classtir
class CountriesSelectView(LocationSelectViewBase):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    
    def get(self, request, *args, **kwargs):
        return self.select_location(request, 'Country')

    def delete(self, request, *args, **kwargs):
        return self.deselect_location(request)
    
# deselect api endpointi icin olusturulmus classtir
class DeselectLocationView(APIView):
    def get(self, request, *args, **kwargs):
        if 'selected_location' in request.session:
            del request.session['selected_location']
            request.session.save()

        return Response('Mevcut session kaldirildi.', status=status.HTTP_200_OK)

####################### ORTAK GOREVLER BITIS #######################


####################### GOREVLER BASLANGIC #######################

# country-most-searched-cities endpointi icin olusturulmustur
class CountryMostSearchedCitiesAPI(APIView):
    def get(self, request):
        country_codes = request.query_params.getlist('country_code')

        if not country_codes:
            return Response({'error': 'En az bir ülke kodu gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        results = []

        for country_code in country_codes:
            cities = City.objects.filter(country__code=country_code).order_by('-search_count')[:5]

            city_data = [{'name': city.name, 'search_count': city.search_count} for city in cities]
            results.append({'country_code': country_code, 'cities': city_data})

        return Response(results)


# country-searched-ratio endpointi icin olusturulmustur
class CountrySearchRatioAPI(APIView):
    def get(self, request):
        country_codes = request.query_params.getlist('country_code')

        if not country_codes:
            return Response({'error': 'En az bir ülke kodu gereklidir.'}, status=status.HTTP_400_BAD_REQUEST)

        results = []

        for country_code in country_codes:
            country = Country.objects.get(code=country_code)
            total_city_search_count = City.objects.filter(country=country).aggregate(total_search_count=Sum('search_count'))['total_search_count'] or 0
            total_airport_search_count = Airport.objects.filter(city__country=country).aggregate(total_search_count=Sum('search_count'))['total_search_count'] or 0

            ratio = total_city_search_count / total_airport_search_count if total_airport_search_count != 0 else 0
            results.append({'country_code': country_code, 'search_ratio': ratio, 'country_name': country.name})

        return Response(results)
####################### GOREVLER BITIS #######################
