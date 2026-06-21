from .models import Country, City, Property, Amenity
from modeltranslation.translator import TranslationOptions,register


@register(Country)
class CountryTranslationOptions(TranslationOptions):
    fields = ('country_name', )

@register(City)
class CityTranslationOptions(TranslationOptions):
    fields = ('city_name', )

@register(Property)
class PropertyCategoryTranslationOptions(TranslationOptions):
    fields = ('property_name', 'description', 'address', )

@register(Amenity)
class AmenityTranslationOptions(TranslationOptions):
    fields = ('name', )

