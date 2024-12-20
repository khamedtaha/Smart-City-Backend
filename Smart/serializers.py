from rest_framework import serializers

from .models import *


class HotelSerializer(serializers.ModelSerializer):
   images_hotel = serializers.SerializerMethodField() 
   hotel_offre_base = serializers.SerializerMethodField()
   class Meta:
      model = Hotel
      fields = '__all__'

   def get_images_hotel(self, obj):
      request = self.context.get('request')  
      return [
            {
               'id': image.id,
               'image_url': request.build_absolute_uri(image.image.url) if request else image.image.url,
               'description': image.description
            }
            for image in obj.images_hotel.all()
      ]
   def get_hotel_offre_base(self, obj):
      return [
            {
               'id': offre.id,
               'name': offre.name,
               'prix': offre.prix
            }
            for offre in obj.hotel_offre.filter(is_base=True)  # Only include offers where is_base=True
      ]

class PlaceImageSerializer(serializers.ModelSerializer):
   class Meta:
      model = PlaceImage
      fields = ['id', 'image', 'description']

class PlaceTypeSerializer(serializers.ModelSerializer):
   class Meta:
      model = PlaceType
      fields = '__all__'


class PlaceSerializer(serializers.ModelSerializer):
   images_place = PlaceImageSerializer(many=True, read_only=True)  
   place_type = PlaceTypeSerializer(read_only=True)  

   class Meta:
      model = Place
      fields = ['id', 'name', 'place_type', 'description', 'cover_image', 'loction', 'images_place']