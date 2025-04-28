from django.contrib import admin
from .models import Glassone, Glasstwo, Glassthree, Szyba, Ramka,AccessKey
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.views.generic import TemplateView
from django.views import View
from django.http import HttpResponse




class Glassoneadmin(admin.ModelAdmin):
    list_display = ('szyba1','gfactor','ufactor','rw')
class Glasstwoadmin(admin.ModelAdmin):
    list_display =('szyba1','ramka1','szyba2','grubosc_calkowita','gfactor','ufactor','rw')
class Glassthreeadmin(admin.ModelAdmin):
    list_display = ('szyba1','ramka1','szyba2','ramka2','szyba3','grubosc_calkowita','gfactor','ufactor','rw')
    list_per_page = 10

class SzybaAdmin(admin.ModelAdmin):
        list_display = ('nazwa', 'grubosc', 'image_display')

        def image_display(self, obj):
            if obj.image:
                return mark_safe(f'<img src="{obj.image.url}" width="100" height="100" />')
            return "Brak obrazu"

        image_display.allow_tags = True
# Rejestracja modeli w adminie
admin.site.register(Glassone,Glassoneadmin)
admin.site.register(Glasstwo,Glasstwoadmin)
admin.site.register(Glassthree,Glassthreeadmin)
admin.site.register(Szyba,SzybaAdmin)
admin.site.register(Ramka)
admin.site.register(AccessKey)


# Register your models here.
