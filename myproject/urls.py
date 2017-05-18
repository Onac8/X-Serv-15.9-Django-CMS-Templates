from django.conf.urls import include, url
from django.contrib import admin
from cms_templates import views

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.home, name="Pagina Principal"),
    url(r'^logout', views.logout, name="Pagina de desconexion"),
    url(r'^annotated/(.+)', views.template, name="Pagina del recurso con template"),
    url(r'^(.+)', views.resource, name="Pagina del recurso"),

]
