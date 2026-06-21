from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.validators import MaxValueValidator, MinValueValidator


USER_ROLE = (
('guest', 'guest'),
('host', 'host')
)
class User(AbstractUser):
    age = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(16), MaxValueValidator(90)])
    role = models.CharField(max_length=6, choices=USER_ROLE, default='guest')
    phone_number = PhoneNumberField(region='KG', default='+996')
    avatar = models.ImageField(upload_to='avatar_image/', null=True, blank=True)


class Country(models.Model):
    country_name = models.CharField(max_length=32, unique=True)

    def __str__(self):
        return self.country_name


class City(models.Model):
    city_name = models.CharField(max_length=32)

    def __str__(self):
        return self.city_name


class Amenity(models.Model):
    name = models.CharField(max_length=32)
    icon = models.ImageField(upload_to='amenity_icon/')

    def __str__(self):
        return self.name


class Property(models.Model):
    property_name = models.CharField(max_length=62)
    price_per_night = models.PositiveSmallIntegerField(default=0)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='city_properties')
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    address = models.CharField(max_length=100)
    PROPERTY_TYPE = (
    ('apartment', 'apartment'),
    ('house', 'house'),
    ('studio', 'studio')
    )
    property_type = models.CharField(max_length=9, choices=PROPERTY_TYPE)
    RULES_TYPE = (
    ('no_smoking', 'no_smoking'),
    ('pets_allowed', 'pets_allowed'),
    ('etc', 'etc')
    )
    rules = models.CharField(max_length=15, choices=RULES_TYPE)
    max_guests = models.PositiveSmallIntegerField()
    bedrooms = models.CharField(max_length=32)
    bathrooms = models.CharField(max_length=32)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='properties')
    property_image = models.ImageField(upload_to='property_images/')
    amenity = models.ManyToManyField(Amenity)
    is_active = models.DateTimeField(auto_now_add=True)
    description = models.TextField()

    def __str__(self):
        return self.property_name


    def get_avg_rating(self):
        reviews = self.property_reviews.all()
        if reviews.exists():
            return sum([i.stars for i in reviews]) / reviews.count()
        return 0

    def get_count_rating(self):
        reviews = self.property_reviews.all()
        if reviews.exists():
            return reviews.count()
        return 0


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_images')
    property_image = models.ImageField(upload_to='images_property')


class Booking(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    guest = models.ForeignKey(User, on_delete=models.CASCADE)
    check_in = models.DateField()
    check_out = models.DateField()
    BOOKING_TYPE = (
    ('pending', 'pending'),
    ('approved', 'approved'),
    ('rejected', 'rejected'),
    ('cancelled', 'cancelled')
    )
    status = models.CharField(max_length=9, choices=BOOKING_TYPE)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.guest}: property: {self.property}'


class Review(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_reviews')
    guest = models.ForeignKey(User,  on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=[(i, str(i))for i in range(1, 11)], null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.guest} : {self.property}'


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    like = models.BooleanField(default=False)






