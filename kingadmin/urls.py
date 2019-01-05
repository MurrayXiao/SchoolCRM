
from django.urls import path
from django.conf.urls import url, include
from kingadmin import views

urlpatterns = [
    url(r'^$', views.app_index, name='app_index'),
    url(r'^(\w+)$', views.app_components, name='app_components'),
    url(r'^(\w+)/(\w+)/$', views.table_obj_list, name='table_obj_list'),
    url(r'^(\w+)/(\w+)/(\d+)/change/$', views.table_obj_change, name='table_obj_change'),
    url(r'^(\w+)/(\w+)/add/$', views.table_obj_add, name='table_obj_add'),
    url(r'^(\w+)/(\w+)/(\d+)/delete$', views.table_obj_delete, name='table_obj_delete'),

    url(r'^login.html', views.acc_login),
    url(r'^logout.html$', views.acc_logout, name='logout.html'),
]
