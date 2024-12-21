from django.contrib import admin


admin.site.site_header = "Admin Panel"
admin.site.site_title = "Panel"


#------------------------------------------

from django.contrib import admin
from .models import *

# Inline for HaubergeImage
class HaubergeImageInline(admin.TabularInline):
   model = HaubergeImage
   extra = 1  # Number of empty forms displayed for new images


# Inline for HaubergeOffre
class HaubergeOffreInline(admin.TabularInline):
   model = HaubergeOffre
   extra = 1  # Number of empty forms displayed for new offers




class HaubergeAdmin(admin.ModelAdmin):
   list_display = ('nom', 'type', 'capacite', 'telephone', 'disponibilite')
   list_filter = ('type', 'disponibilite')
   inlines = [HaubergeImageInline, HaubergeOffreInline]
   ordering = ('nom',)


admin.site.register(Hauberge, HaubergeAdmin)
# Admin configuration for HaubergeImage
@admin.register(HaubergeImage)
class HaubergeImageAdmin(admin.ModelAdmin):
   list_display = ('hauberge', 'image', 'description')
   search_fields = ('hauberge__nom', 'description')
   list_filter = ('hauberge',)


# Admin configuration for HaubergeOffre
@admin.register(HaubergeOffre)
class HaubergeOffreAdmin(admin.ModelAdmin):
   list_display = ('hauberge', 'titre', 'prix')
   search_fields = ('titre', 'description', 'hauberge__nom')
   list_filter = ('hauberge',)

# Admin for Resident
@admin.register(Resident)
class ResidentAdmin(admin.ModelAdmin):
   list_display = ('nom', 'prenom', 'date_naissance', 'sexe', 'numero_carte_identite', 'permission_parentale')
   list_filter = ('sexe', 'permission_parentale')
   search_fields = ('nom', 'prenom', 'numero_carte_identite')
   ordering = ('nom', 'prenom')


# Admin for BlackList
@admin.register(BlackList)
class BlackListAdmin(admin.ModelAdmin):
   list_display = ('nom', 'prenom', 'numero_carte_identite')
   search_fields = ('nom', 'prenom', 'numero_carte_identite')
   ordering = ('nom', 'prenom')

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
   list_display = ('hauberge', 'resident', 'numero_chambre', 'date_entree', 'date_sortie', 'nature_reservation', 'restauration_montant')
   list_filter = ('nature_reservation', 'date_entree', 'date_sortie')
   search_fields = ('hauberge__nom', 'resident__nom', 'resident__prenom')
   ordering = ('date_entree', 'date_sortie')


# Admin for HaubergeResident
@admin.register(HaubergeResident)
class HaubergeResidentAdmin(admin.ModelAdmin):
   list_display = ('hauberge', 'resident')
   search_fields = ('hauberge__nom', 'resident__nom', 'resident__prenom')
   ordering = ('hauberge', 'resident')