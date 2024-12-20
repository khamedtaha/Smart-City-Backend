from django.db import models
from location_field.models.plain import PlainLocationField



class Hotel(models.Model):
   TYPE_CHOICES = [
      (1, '1 Star'),
      (2, '2 Stars'),
      (3, '3 Stars'),
      (4, '4 Stars'),
      (5, '5 Stars'),
   ]

   nom = models.CharField(max_length=255)
   description = models.CharField(max_length=255, blank=True, null=True)
   type = models.IntegerField(choices=TYPE_CHOICES, verbose_name="Hotel Type")  # Type field with choices
   web_site = models.URLField(verbose_name="Web site Hotel", blank=True, null=True)
   cover_image = models.ImageField(upload_to='hotel_covers/', verbose_name="Cover Image", blank=True, null=True)  # Cover Image field
   loction = PlainLocationField(blank = True) 
   def __str__(self):
      return f"{self.nom}"

class HotelImage(models.Model):
   hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='images_hotel')
   image = models.ImageField(upload_to='hotel_images/')  # Upload image file or path
   description = models.CharField(max_length=255, blank=True, null=True)  # Optional image description

   def __str__(self):
      return f"Image for {self.hotel.nom}"
   




class PlaceType(models.Model):
   name = models.CharField(max_length=100, unique=True)  

   def __str__(self):
      return self.name
   
class Place(models.Model):
   name = models.CharField(max_length=255)  
   place_type = models.ForeignKey(PlaceType, on_delete=models.SET_NULL, verbose_name="Place Type" , null = True , blank = True)  
   description = models.TextField(blank=True, null=True)  
   cover_image = models.ImageField(upload_to='place_covers/', verbose_name="Cover Image Plase", blank=True, null=True) 
   loction = PlainLocationField(blank = True)
   def __str__(self):
      return f"{self.name} ({self.place_type})"



class PlaceHotelRelation(models.Model):
   place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='place_hotels')
   hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='hotel_places')
   distance = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Distance (km)", blank=True, null=True)
   is_nearby = models.BooleanField(default=True, verbose_name="Is Nearby?")  





class PlaceImage(models.Model):
   place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='images_place')
   image = models.ImageField(upload_to='place_images/')  # Upload image file or path
   description = models.CharField(max_length=255, blank=True, null=True)  # Optional image description

   def __str__(self):
      return f"Image for {self.place.name}"