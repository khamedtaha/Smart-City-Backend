from django.contrib import admin
from .models import * 


# Admin class for HotelImage (Inline)
class HotelImageInline(admin.TabularInline):  # Use TabularInline for a tabular layout
   model = HotelImage
   extra = 1  # Number of empty image forms to display

# Admin class for Hotel
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
   list_display = ('nom', 'type', 'web_site', 'cover_image')  # Columns to display in the admin list view
   list_filter = ('type',)  # Filter hotels by type
   search_fields = ('nom', 'description')  # Add a search bar for hotel name and description
   inlines = [HotelImageInline]  # Add inline images
   #readonly_fields = ['cover_image']  # Preview cover image in the form view

@admin.register(HotelImage)
class HotelImageAdmin(admin.ModelAdmin):
   list_display = ('hotel', 'image', 'description')
   search_fields = ('hotel__nom', 'description')


# PlaceHotelRelation Inline
class PlaceHotelRelationInline(admin.TabularInline):
   model = PlaceHotelRelation
   extra = 1


# PlaceImage Inline
class PlaceImageInline(admin.TabularInline):
   model = PlaceImage
   extra = 1


# PlaceType Admin
@admin.register(PlaceType)
class PlaceTypeAdmin(admin.ModelAdmin):
   list_display = ('name',)
   search_fields = ('name',)

@admin.register(HotelOffre)
class PlaceTypeAdmin(admin.ModelAdmin):
   list_display = ('name', 'is_base' , 'prix'  ,'hotel')
   search_fields = ('name', 'prix')

# Place Admin
@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
   list_display = ('name', 'place_type', 'description')
   search_fields = ('name', 'description')
   list_filter = ('place_type',)
   inlines = [PlaceHotelRelationInline, PlaceImageInline]
