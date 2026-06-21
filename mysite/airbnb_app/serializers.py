from rest_framework import serializers
from .models import (User, Country, City, Amenity, Property,
                     PropertyImage, Booking, Review, Favorite)
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'age',
                  'phone_number', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Неверные учетные данные")

    def to_representation(self, instance):
        refresh = RefreshToken.for_user(instance)
        return {
            'user': {
                'username': instance.username,
                'email': instance.email,
            },
            'access': str(refresh.access_token),
            'refresh': str(refresh),
        }


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class CountrySerializers(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class CityListSerializers(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'city_name']


class AmenitySerializers(serializers.ModelSerializer):
    class Meta:
        model = Amenity
        fields = ['id', 'name']


class PropertyListSerializers(serializers.ModelSerializer):
    owner = UserSerializers()
    country = CountrySerializers()
    city = CityListSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'get_avg_rating', 'get_count_rating', 'description', 'price_per_night',
                  'city', 'country', 'property_type', 'rules', 'max_guests', 'owner', 'property_image']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class PropertyImageSerializers(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['id', 'property_image']


class PropertySimpleSimpleSerializers(serializers.ModelSerializer):
    class Meta:
        model = Property
        fields = ['id', 'property_name']


class BookingSerializers(serializers.ModelSerializer):
    property = PropertySimpleSimpleSerializers()
    guest = UserSerializers()
    class Meta:
        model = Booking
        fields = ['id', 'property', 'guest', 'check_in', 'check_out', 'status', 'created_at']


class ReviewSerializers(serializers.ModelSerializer):
    guest = UserSerializers()
    property = PropertySimpleSimpleSerializers
    class Meta:
        model = Review
        fields = ['id', 'property', 'guest', 'rating', 'comment', 'created_at']


class PropertySimpleSerializers(serializers.ModelSerializer):
    country = CountrySerializers()
    class Meta:
        model = Property
        fields = ['id', 'property_image', 'property_name', 'country']


class CityDetailSerializers(serializers.ModelSerializer):
    city_properties = PropertySimpleSerializers(read_only=True, many=True)
    class Meta:
        model = City
        fields = '__all__'


class PropertyDetailSerializers(serializers.ModelSerializer):
    country = CountrySerializers()
    city = CityListSerializers()
    property_images = PropertyImageSerializers(read_only=True, many=True)
    amenity = AmenitySerializers(many=True)
    property_reviews = ReviewSerializers(read_only=True, many=True)
    owner = UserSerializers()
    get_avg_rating = serializers.SerializerMethodField
    get_count_rating = serializers.SerializerMethodField

    class Meta:
        model = Property
        fields = ['id', 'property_name', 'get_avg_rating', 'get_count_rating', 'description', 'price_per_night',
                  'city', 'country', 'property_type', 'rules', 'max_guests', 'bedrooms', 'bathrooms',
                   'amenity', 'property_image', 'property_images', 'owner',
                   'property_reviews']

    def get_avg_rating(self, obj):
        return obj.get_avg_rating()

    def get_count_rating(self, obj):
        return obj.get_count_rating()


class FavoriteSerializers(serializers.ModelSerializer):
    user = UserSerializers()
    property = PropertySimpleSerializers()
    class Meta:
        model = Favorite
        fields = ['id', 'user', 'property']