from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # location app'i icerisinde tanimlanacak urller 'api/' uzantisina eklenecek 
    path('api/', include('location.urls')),
]
