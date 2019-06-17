from django.contrib import admin

from .models import Region, Port, Price


class RegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent',)
    list_display_links = ('id', 'name',)
    raw_id_fields = ('parent',)
    search_fields = ('name',)


class PortAdmin(admin.ModelAdmin):
    list_display = ('id', 'code', 'name', 'region',)
    list_display_links = ('id', 'code',)
    raw_id_fields = ('region',)
    search_fields = ('code', 'name',)


class PriceAdmin(admin.ModelAdmin):
    list_display = ('id', 'origin', 'destination', 'day', 'price')
    raw_id_fields = ('origin', 'destination')
    search_fields = ('origin', 'destination', 'day')


admin.site.register(Region, RegionAdmin)
admin.site.register(Port, PortAdmin)
admin.site.register(Price, PriceAdmin)
