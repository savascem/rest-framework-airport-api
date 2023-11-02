from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Country, City, Airport
from .serializers import CountrySerializer
from .helpers.test_utils import selection_test_helper, session_selection_test_helper, most_searched_test_helper


# location modellerinin search api endpointleri icin test case
class CountryAPITest(APITestCase):

    def test_country_search(self):
        
        response = self.client.get(reverse('country-search'), {'query': 'tÜRKİyE'})

        country = Country.objects.get(code='TR')
        serializer = CountrySerializer(country)
        
        # self.assertEqual(response.data, {'countries' :serializer.data})
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# location modellerinin selection api endpointleri icin test case
class LocationSelectAPITest(APITestCase):

    # airport selection durumu icin test
    def test_airports_select(self):

        airport_count, city_count, country_count, session_state1, session_state2, airport2 = selection_test_helper(self, pk=3, model_title='Airport', Country=Country, City=City)

        self.assertEqual(True, session_state1 & session_state2)
        self.assertEqual(True, airport_count & city_count & country_count)
        self.assertEqual(airport2.status_code, status.HTTP_200_OK)

    # city selection durumu icin test
    def test_city_select(self):

        city_count, country_count, session_state1, session_state2, city2 = selection_test_helper(self, pk=21, model_title='City', Country=Country)

        self.assertEqual(True, session_state1 & session_state2)
        self.assertEqual(True, city_count & country_count)
        self.assertEqual(city2.status_code, status.HTTP_200_OK)

    # country selection durumu icin test
    def test_country_select(self):

        country_count, session_state1, session_state2, country2 = selection_test_helper(self, pk=13, model_title='Country')

        self.assertEqual(True, session_state1 & session_state2)
        self.assertEqual(True, country_count)
        self.assertEqual(country2.status_code, status.HTTP_200_OK)


# deselect api endpointi icin test case
class LocationDeselectAPITest(APITestCase):
    def test_location_deselect(self):

        # baslangic oturum None donmesi beklenir
        session0 = self.client.session.get('selected_location')
        session0_state = session0 is None

        # rastgele bir lokasyon secilir ve oturum bilgilerinin rastgele lokasyona gore degismesi beklenir
        session1_state = session_selection_test_helper(self, pk=13, model_title='City')

        # yeni bir lokasyon secilir ve eski lokasyonun otomatik olarak degismis olmasi beklenir.
        session2_state = session_selection_test_helper(self, pk=124, model_title='Airport')

        # deselect islemi sonrasinda mevcut session durumunun None olarak guncellenmesi beklenir.
        deselect = self.client.get(reverse('deselect'))
        session3 = self.client.session.get('selected_location')
        session3_state = session3 is None

        self.assertEqual(True, session0_state & session1_state & session2_state & session3_state)
        self.assertEqual(deselect.status_code, status.HTTP_200_OK)

        
# ulke koduna gore en cok aranan sehirler listesi api endpointi icin test case
class MostSearchedCities(APITestCase):
    def test_most_searched_cities(self):

        city1, city2, city1_count1, city2_count1 = most_searched_test_helper(country_code='US', object=City)

        # veri tabaninda tiklama islemini yapalim
        for _ in range(2):
            session_selection_test_helper(self, pk=city1.id, model_title='City')

        for _ in range(10):
            session_selection_test_helper(self, pk=city2.id, model_title='City')

        city1_, city2_, city1_count2, city2_count2 = most_searched_test_helper(country_code='US', object=City)

        response = self.client.get(reverse('country-most-searched-cities'), {'country_code': 'US'})
        data = response.data[0]

        if (data['cities'][0]['name'] == city2_.name) & (data['cities'][1]['name'] == city1_.name):
            condition = True

        self.assertEqual(True, condition)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


# ulke koduna gore toplam sehir arama sayisi/airport arama sayisinin listelendigi api endpointi icin test case
class CountrySearchedRatioTest(APITestCase):
    def setUp(self):
        self.country = Country.objects.create(
            name="Test Country", code="TEST", phone_code=212121, search_text='x', search_count=0
            )
        self.city1 = City.objects.create(
            name="Test City1", country=self.country, search_text='x', search_count=0
            )
        self.city2 = City.objects.create(
            name="Test City2", country=self.country, search_text='x', search_count=0
            )
        self.airport1 = Airport.objects.create(name="Test Airport1", code='ABCDE', city=self.city1, country=self.country, search_text='x', search_count=0)
        self.airport2 = Airport.objects.create(name="Test Airport2", code='ABCDEF', city=self.city2, country=self.country, search_text='x', search_count=0)

    def test_searched_ratio(self):

        # veri tabaninda yapilacak toplam selection islemi sayilari
        x=13
        y=24
        z=17
        t=6

        airports = Airport.objects.filter(country__code='TEST')

        # airport icin yapilan tiklamalar
        # bu tiklamalar yapilirken parent model olan city icin aramalar da artmali
        for _ in range(x):
            session_selection_test_helper(self, pk=airports[0].id, model_title='Airport')
        for _ in range(y):
            session_selection_test_helper(self, pk=airports[1].id, model_title='Airport')

        # city icin yapilan tiklamalar
        for _ in range(z):
            session_selection_test_helper(self, pk=airports[0].city.id, model_title='City')
        for _ in range(t):
            session_selection_test_helper(self, pk=airports[1].city.id, model_title='City')

        # teorik olarak olmasi gereken ratio = city + airport aramalari / airport aramalari
        ratio_teorik = (x+y+z+t) / (x+y)

        response = self.client.get(reverse('country-searched-ratio'), {'country_code': 'TEST'})

        condition = ratio_teorik == response.data[0]['search_ratio']

        self.assertEqual(True, condition)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

