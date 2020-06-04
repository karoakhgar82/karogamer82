from django.contrib import admin
from . import views
from django.conf.urls import url,include

app_name = "home"

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/',include('accounts.urls')),
    url(r'^Home/',include('Home.urls')),
    url(r'^$',views.homepage,name='homepage' )
]
