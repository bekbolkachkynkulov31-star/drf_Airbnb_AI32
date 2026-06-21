from django.contrib import admin
from .models import (User, Country, City, Amenity, Property,
                     PropertyImage, Booking, Review)

class PropertyImageInline(admin.TabularInline):
    model = PropertyImage
    extra = 1


admin.site.register(User)
admin.site.register(Booking)
admin.site.register(Review)


from modeltranslation.admin import TranslationAdmin
@admin.register(Country, City, Amenity)
class AllAdmin(TranslationAdmin):

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

@admin.register(Property)
class ProductAdmin(TranslationAdmin):
    inlines = [PropertyImageInline]

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'https://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
                'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }