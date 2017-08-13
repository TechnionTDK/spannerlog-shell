from django.conf.urls import url

from . import views

app_name = 'spannerlog'

urlpatterns = [
	# ex: /spannerlog/
    url(r'^$', views.index, name='index'),
    # ex: /spannerlog/run/
    url(r'^run/$', views.run, name='run'),
]
