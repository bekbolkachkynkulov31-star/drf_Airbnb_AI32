from django.urls import path, include
from rest_framework import routers
from .views import (UserViewSet, CountryViewSet, CityListViewSet, CityDetailViewSet, AmenityViewSet,
                    PropertyListViewSet, PropertyDetailViewSet,
                    PropertyImageViewSet, BookingViewSet, ReviewViewSet, RegisterView,
                    CustomLoginView, LogoutView, FavoriteViewSet)

router = routers.DefaultRouter()

router.register(r'user', UserViewSet, basename='user')
router.register(r'country', CountryViewSet, basename='country')
router.register(r'amenity', AmenityViewSet, basename='amenity')
router.register(r'property_image', PropertyImageViewSet, basename='property_image')
router.register(r'booking', BookingViewSet, basename='booking')
router.register(r'review', ReviewViewSet, basename='review')
router.register(r'favorite', FavoriteViewSet, basename='favorite')


urlpatterns = [
    path('', include(router.urls)),

    path('register/', RegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),

    path('city/', CityListViewSet.as_view(), name='city'),
    path('city/<int:pk>/', CityDetailViewSet.as_view(), name='city_detail'),

    path('property/', PropertyListViewSet.as_view(), name='property'),
    path('property/<int:pk>/', PropertyDetailViewSet.as_view(), name='property_detail')
]

