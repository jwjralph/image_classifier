from django.conf.urls import url
from classify.views import list, vote, DView, RView
from . import views

app_name='classify'
urlpatterns = [
    url(r'^list/$', list, name='list'),
    url(r'^results/(?P<pk>[0-9]+)/$', DView.as_view(), name='detail'),
    url(r'^success/(?P<pk>[0-9]+)/$', RView.as_view(), name='results'),
    url(r'^vote/$', vote, name='vote'),  
]

## results needs questionid, detail needs both list neither 


## idea for container id.. Run command i used in terminal last night through the socket.
## Give instruction in the read me to run a shell script which will then identify the id and alter the contents of predict(?) accordingly.
