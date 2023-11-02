* search_text olusturan komut =>  python manage.py search_text_commands
  
## Api Endpointleri

##### Search Api

* country -> http://127.0.0.1:8000/api/search/country/?query={Sorgulanacak Text}
* city -> http://127.0.0.1:8000/api/search/city/?query={Sorgulanacak Text}
* airport -> http://127.0.0.1:8000/api/search/airport/?query={Sorgulanacak Text}

##### Selection Api

* country -> http://127.0.0.1:8000/api/select/country/{Secilecek nesnenin veri tabani pk degeri} 
* city -> http://127.0.0.1:8000/api/select/city/{Secilecek nesnenin veri tabani pk degeri} 
* airport -> http://127.0.0.1:8000/api/select/airport/{Secilecek nesnenin veri tabani pk degeri} 

* deselect -> http://127.0.0.1:8000/api/deselect/

##### Country Most Searched Cities Api

* http://127.0.0.1:8000/api/country-most-searched-cities/?country_code={Ulke Kodu}&country_code={Ulke Kodu} ....

##### Country Search Ratio Api

* http://127.0.0.1:8000/api/country-searched-ratio/?country_code={Ulke Kodu}&country_code={Ulke Kodu} ....

# PostgreSQL connection

* proje kok dizini settings klasoru icinde veritabani adi ve sifre doldurulmali.
* PostgreSQL'in unaccent arama desteklemesi icin 'CREATE EXTENSION unaccent;' kodu calistirilmali