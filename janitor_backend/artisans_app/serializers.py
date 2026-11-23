from rest_framework import serializers
from django.contrib.gis.geos import Point

# local imports
from .models import (
    ArtisanProfile,
    ProfessionalQualifications,
    Rating,
    JobProposal
)
from .validators import validate_image_size, image_extension_validator


class ArtisanProfileSerializer(serializers.ModelSerializer):
    # average_rating = serializers.SerializerMethodField()
    profile_image = serializers.ImageField(
        validators=[
            validate_image_size,
            image_extension_validator
        ]
    )
    latitude = serializers.FloatField(
        write_only=True,
        min_value=-90,
        max_value=90
    )
    longitude = serializers.FloatField(
        write_only=True,
        min_value=-180,
        max_value=180
    )

    class Meta:
        model = ArtisanProfile
        fields = '__all__'
        read_only_fields = ['user']
    
    def create(self, validated_data):
        latitude = validated_data.pop("latitude")
        longitude = validated_data.pop("longitude")

        point = Point(longitude, latitude, srid=4326)
        validated_data["location"] = point

        return super().create(validated_data)
    

class ProfessionalQualificationsSerializer(serializers.ModelSerializer):
    file = serializers.ImageField(
        validators=[
            validate_image_size
        ]
    )
    
    class Meta:
        model = ProfessionalQualifications
        fields = ['id', 'title','file', 'file_description']
        read_only_fields = ['id']


class RatingSerializer(serializers.ModelSerializer):
    '''Serializer for Rating Data'''
    
    class Meta:
        model = Rating
        fields = ['comment', 'rate_score']


class JobProposalSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        fields = ['description', 'price', 'location']

class JobProposalResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobProposal
        fields = "__all__"


class LocationSerializer(serializers.Serializer):
    latitude = serializers.FloatField(
        min_value=-90,
        max_value=90
    )
    longitude = serializers.FloatField(
        min_value=-180,
        max_value=180
    )


# class NearbyArtisanSerializer(serializers.ModelSerializer):

#     username = serializers.CharField(
#         source="user.username",
#         read_only=True
#     )

#     distance_km = serializers.SerializerMethodField()

#     class Meta:
#         model = ArtisanProfile
#         fields = [
#             "id",
#             "username",
#             "profile_image",
#             "phone_number",
#             "bio_headline",
#             "bio",
#             "address",
#             "distance_km",
#             "is_available",
#             "verification_status",
#         ]

#     def get_distance_km(self, obj):
#         return round(obj.distance.km, 2)


class NearbyArtisanSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    distance_km = serializers.SerializerMethodField()
    latitude = serializers.SerializerMethodField()
    longitude = serializers.SerializerMethodField()

    class Meta:
        model = ArtisanProfile
        fields = [
            "id",
            "username",
            "profile_image",
            "phone_number",
            "bio_headline",
            "bio",
            "address",
            "distance_km",
            "is_available",
            "verification_status",
            "latitude",
            "longitude",
        ]

    def get_distance_km(self, obj):
        return round(obj.distance.km, 2)

    def get_latitude(self, obj):
        return obj.location.y if obj.location else None

    def get_longitude(self, obj):
        return obj.location.x if obj.location else None