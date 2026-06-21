from rest_framework import viewsets, filters, generics, status, permissions

from .models import (User, Country, City, Amenity, Property,
                     PropertyImage, Booking, Review, Favorite)
from .serializers import (UserSerializers, CountrySerializers, CityListSerializers, CityDetailSerializers,
                          AmenitySerializers, PropertyListSerializers, PropertyDetailSerializers,
                          PropertyImageSerializers, FavoriteSerializers,
                          BookingSerializers, ReviewSerializers, RegisterSerializer, LoginSerializer)
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .filter import PropertyFilter
from .pagination import PropertyPagination

from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .permission import CheckRole, CheckOwner


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CustomLoginView(TokenObtainPairView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response({"detail": "Неверные учетные данные"}, status=status.HTTP_401_UNAUTHORIZED)

        user = serializer.validated_data
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutView(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers


class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializers
    filter_backends = [SearchFilter]
    search_fields = ['country_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityListViewSet(generics.ListAPIView):
    queryset = City.objects.all()
    serializer_class = CityListSerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['city_name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class CityDetailViewSet(generics.RetrieveAPIView):
    queryset = City.objects.all()
    serializer_class = CityDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class AmenityViewSet(viewsets.ModelViewSet):
    queryset = Amenity.objects.all()
    serializer_class = AmenitySerializers
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class PropertyListViewSet(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyListSerializers
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['property_name', 'city']
    filterset_class = PropertyFilter
    pagination_class = PropertyPagination
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckRole]


class PropertyDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertyDetailSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, CheckOwner]


class PropertyImageViewSet(viewsets.ModelViewSet):
    queryset = PropertyImage.objects.all()
    serializer_class = PropertyImageSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookingViewSet(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializers
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


