from django_filters.rest_framework import FilterSet
from .models import Property


class PropertyFilter(FilterSet):
    class Meta:
        model = Property
        fields = {
            'country': ['exact'],
            'city': ['exact'],
            'amenity': ['exact']
        }