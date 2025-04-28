
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import Szyby,Ramki,index,pakiet_jednoszybowy,pakiet_dwuszybowy,pakiet_trzyszybowy,create_pakiet
from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LogoutView
from .views import render_pdf ,delete_pakiet1,delete_pakiet2,delete_pakiet3,edit_pakiet,edit_pakiet1,edit_pakiet2
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ExportXlsxView
from django.urls import path
from .views import ExportCsvView
from .views import import_csv_view ,import_xlsx_view,html_to_xml_view2,html_to_xml_view1,json_to_xml_view

from .views import (
    RamkaAPIView,
    SzybaAPIView,
    Pakiet_jednoszybowyAPIView,
    Pakiet_dwuszybowyAPIView,
    Pakiet_trzyszybowyAPIView
)

urlpatterns = [
    path('', index.as_view(), name='index'),
    path('pakiet_jednoszybowy/', pakiet_jednoszybowy.as_view(), name='pakiet_jednoszybowy'),
    path('pakiet_dwuszybowy/', pakiet_dwuszybowy.as_view(), name='pakiet_dwuszybowy'),
    path('pakiet_trzyszybowy/', pakiet_trzyszybowy.as_view(), name='pakiet_trzyszybowy'),
    path('api/pakiet_trzyszybowy/', Pakiet_trzyszybowyAPIView.as_view(), name='api_pakiet_trzyszybowy'),
    path('api/pakiet_jednoszybowy/',Pakiet_jednoszybowyAPIView.as_view(),name='api_pakiet_jednosobowy'),
    path('api/pakiet_dwuszybowy/',Pakiet_dwuszybowyAPIView.as_view(),name='api_pakiet_dwuszybowy'),
    #path('pakiet_jednoszybowy/', views.pakiet_jednoszybowy, name='pakiet_jednoszybowy'),
    #path('pakiet_dwuszybowy/', views.pakiet_dwuszybowy, name='pakiet_dwuszybowy'),
    #path('pakiet_trzyszybowy/', views.pakiet_trzyszybowy, name='pakiet_trzyszybowy'),
    path('szyby/', Szyby.as_view(), name='szyby'),
    path('ramki/', Ramki.as_view(), name='ramki'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('pdfg2/', render_pdf, name='pdfg2'),
    path('pdfg3/', render_pdf, name='pdfg3'),
    path('pdfg1/', render_pdf, name='pdfg1'),
    path('pdfr/', render_pdf, name='pdfr'),
    path('pdfs/', render_pdf, name='pdfs'),
    path('aramki/', RamkaAPIView.as_view(), name='ramka-list-create'),
    path('aszyby/', SzybaAPIView.as_view(), name='szyba-list-create'),
    path('ap1/', Pakiet_jednoszybowyAPIView.as_view(), name='glassone-list-create'),
    path('ap2/', Pakiet_dwuszybowyAPIView.as_view(), name='glasstwo-list-create'),
    path('ap3/', Pakiet_trzyszybowyAPIView.as_view(), name='glassthree-list-create'),
    path('create_pakiet/', views.create_pakiet, name='create_pakiet'),
    path('create_pakiet1/', views.create_pakiet1, name='create_pakiet1'),
    path('create_pakiet2/', views.create_pakiet2, name='create_pakiet2'),
    path('api/pakiet_trzyszybowy/delete/', delete_pakiet3.as_view(), name='delete_pakiet'),
    path('api/pakiet_dwuszybowy/delete/', delete_pakiet2.as_view(), name='delete_pakiet'),
    path('api/pakiet_jednoszybowy/delete/', delete_pakiet1.as_view(), name='delete_pakiet'),
    path('api/pakiet_trzyszybowy/update/', edit_pakiet.as_view(), name='edit_pakiet'),
    path('api/pakiet_jednoszybowy/update/', edit_pakiet1.as_view(), name='edit_pakiet1'),
    path('api/pakiet_dwuszybowy/update/',edit_pakiet2.as_view(),name='edit_pakiet2'),
    path('export-xlsx/', ExportXlsxView.as_view(), name='export_xlsx'),
    path('export-csv/', ExportCsvView.as_view(), name='export_csv'),
    path('import_csv/', import_csv_view, name='import_csv'),
    path('import_xlsx/', import_xlsx_view, name='import_xlsx'),
    path('xml2/',html_to_xml_view2,name='xml2'),
    path('xml1/',html_to_xml_view1,name='xml1'),
    path('xml3/',json_to_xml_view,name='xml3')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
