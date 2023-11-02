from django.urls import reverse    
import time


def selection_test_helper(self, pk, model_title, Country=None, City=None, Airport=None):
    
    url = reverse(f'select_{model_title.lower()}', kwargs={'pk': pk})

    # get request islemi oncesinde oturum kontrolu
    selected_location1 = self.client.session.get('selected_location')
    print('guncel oturum:', selected_location1)

    # ilk get request atilir. bu noktada airport, city ve country alanlarının search count degerleri saklanir.
    if model_title == 'Airport':
        airport1 = self.client.get(url)
        country1 = Country.objects.get(id=airport1.data['country'])
        city1 = City.objects.get(id=airport1.data['city'])
    elif model_title == 'City':
        city1 = self.client.get(url)
        country1 = Country.objects.get(id=city1.data['country'])
    elif model_title == 'Country':
        country1 = self.client.get(url)

    # get request islemi sonrasinda oturum kontrolu
    selected_location2 = self.client.session.get('selected_location')
    print('guncel oturum:', selected_location2)

    time.sleep(0.3)

    # ikinci get request atilir. bu noktada airport, city ve country alanlarının 
    # search count degerlerinde +1 artis gozlenmesi beklenir
    if model_title == 'Airport':
        airport2 = self.client.get(url)
        country2 = Country.objects.get(id=airport2.data['country'])
        city2 = City.objects.get(id=airport2.data['city'])
    elif model_title == 'City':
        city2 = self.client.get(url)
        country2 = Country.objects.get(id=city2.data['country'])
    elif model_title == 'Country':
        country2 = self.client.get(url)


    # airport, city ve country alanlarının search count degerlerinde artis olma durumunun sorgusu yapilir.
    if model_title == 'Airport':
        airport_count = airport1.data['search_count'] + 1 == airport2.data['search_count']
        city_count = city1.search_count + 1 == city2.search_count
        country_count = country1.search_count + 1 == country2.search_count
    elif model_title == 'City':
        city_count = city1.data['search_count'] + 1 == city2.data['search_count']
        country_count = country1.search_count + 1 == country2.search_count
    elif model_title == 'Country':
        country_count = country1.data['search_count'] + 1 == country2.data['search_count']


    # oturum bilgilerinin baslangista None olmasi ve 
    # get isleminde sonra oturum isleminin degismesi sorgusu yapilir
    session_state1 = selected_location1 is None
    session_state2 = selected_location2 == f'{model_title}_{pk}'

    if model_title == 'Airport':
        return airport_count, city_count, country_count, session_state1, session_state2, airport2
    
    elif model_title == 'City':
        return city_count, country_count, session_state1, session_state2, city2
    
    elif model_title == 'Country':
        return country_count, session_state1, session_state2, country2

def session_selection_test_helper(self, pk, model_title):

    url = reverse(f'select_{model_title.lower()}', kwargs={'pk': pk})
    selection = self.client.get(url)
    session = self.client.session.get('selected_location')

    session_state = session == f"{model_title}_{pk}"

    return session_state

def most_searched_test_helper(object, country_code):
    cities = object.objects.filter(country__code=country_code)

    city1 = cities[0]
    city2 = cities[1]

    city1_count_1 = city1.search_count
    city2_count_1 = city2.search_count

    return city1, city2, city1_count_1, city2_count_1