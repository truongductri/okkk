
from django.conf.urls import include, url
from django.contrib import admin
from . import views#, excel
from excel import export
import quicky
app=quicky.applications.get_app_by_file(__file__)
from django.conf.urls.static import static
import os
app=quicky.applications.get_app_by_file(__file__)
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login$',views.login,name='logn'),
    url(r'^pages/(?P<path>.*)$', views.load_page, name='singleshop'),
    #url(r'^list/(?P<path>.*)$', views.load_list, name='singleshop'),
    url(r'^sign_out',views.sign_out),
    url(r'^api$',"quicky.api.call"),
    url(r'^excel_export$', export.call, name='excel_export'),
    #url(r'^file/download', views.file_download),
    #url(r'^excel_template/(?P<path>.*)$', 'django.views.static.serve', 
    #    {
    #        'document_root': os.getcwd() + os.path.sep + ('/excel_template/'.replace("/", os.path.sep)), 
    #        'show_indexes': True 
    #    }
    #),
    app.get_static_urls()
]

