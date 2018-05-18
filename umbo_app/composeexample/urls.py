from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'^classify/', include('classify.urls')),
    url(r'^admin/', admin.site.urls),
]
