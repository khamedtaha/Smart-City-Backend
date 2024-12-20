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
    def get_queryset(self, request):
        # تحديد البيانات المعروضة حسب المستخدم
        qs = super().get_queryset(request)
        if request.user.is_superuser:  # المشرف يرى كل البيانات
            return qs
        return qs.filter(user=request.user)  # المستخدم يرى بياناته فقط

    def save_model(self, request, obj, form, change):
        # تعيين المستخدم الحالي عند حفظ النموذج
        if not obj.pk:  # إضافة جديدة
            obj.user = request.user
        super().save_model(request, obj, form, change)

    def has_change_permission(self, request, obj=None):
        # السماح بالتعديل فقط إذا كان مرتبطًا بالمستخدم
        if obj and obj.user != request.user:
            return False
        return super().has_change_permission(request, obj)

    def has_delete_permission(self, request, obj=None):
        # السماح بالحذف فقط إذا كان مرتبطًا بالمستخدم
        if obj and obj.user != request.user:
            return False
        return super().has_delete_permission(request, obj)

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