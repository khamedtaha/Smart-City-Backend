from django.db import models

from django.contrib.auth.models import User
from location_field.models.plain import PlainLocationField


class Hauberge(models.Model):
   TYPE_CHOICES = [
      ('maison', 'Maison'),
      ('camp', 'Camp'),
   ]
   
   user = models.OneToOneField(User , blank = False , on_delete = models.CASCADE)
   type = models.CharField(max_length=10, choices=TYPE_CHOICES)
   capacite = models.IntegerField()
   nom = models.CharField(max_length=255)
   emplacement = PlainLocationField(blank = True)  # Coordonnées GPS
   adresse = models.CharField(max_length=255)
   telephone = models.CharField(max_length=20)
   nbr_personne_reserve = models.IntegerField()
   disponibilite = models.BooleanField(default=True)

   def __str__(self):
      return self.nom

class HaubergeImage(models.Model):
   hauberge = models.ForeignKey(Hauberge, on_delete=models.CASCADE, related_name='images')
   image = models.ImageField(upload_to='hauberge_images/')  # Upload image file or path
   description = models.CharField(max_length=255, blank=True, null=True)  # Optional image description

   def __str__(self):
      return f"Image for {self.hauberge.nom}"
   
class HaubergeOffre(models.Model):
   hauberge = models.ForeignKey(Hauberge, on_delete=models.CASCADE, related_name='offres')
   titre = models.CharField(max_length=255)  # Titre de l'offre
   description = models.TextField()  # Description de l'offre
   prix = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Prix optionnel

   def __str__(self):
      return f"Offre: {self.titre} for {self.hauberge.nom}"
   

#-----------------------------------------------------------------------------


class Resident(models.Model):
   user = models.OneToOneField(User , blank = False , on_delete = models.CASCADE)
   SEXE_CHOICES = [
      ('Homme', 'Homme'),
      ('Femme', 'Femme'),
   ]

   nom = models.CharField(max_length=255 , blank= True , null = True)
   prenom = models.CharField(max_length=255 , blank= True , null = True)
   date_naissance = models.DateField(blank= True , null = True)
   lieu_naissance = models.CharField(max_length=255, blank= True , null = True)
   sexe = models.CharField(max_length=10, choices=SEXE_CHOICES, blank= True , null = True)
   numero_carte_identite = models.CharField(max_length=50, unique=True, blank= True , null = True)
   permission_parentale = models.BooleanField(blank= True , null = True)

   def __str__(self):
      return f"{self.nom} {self.prenom}"
   
class BlackList(models.Model):
   nom = models.CharField(max_length=255)
   prenom = models.CharField(max_length=255)
   numero_carte_identite = models.CharField(max_length=50, unique=True)

   def __str__(self):
      return f"{self.nom} {self.prenom}"

class Reservation(models.Model):
   NATURE_CHOICES = [
      ('Gratuit', 'Gratuit'),
      ('Non Gratuit', 'Non Gratuit'),
   ]

   hauberge = models.ForeignKey(Hauberge, on_delete=models.CASCADE)
   resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
   numero_chambre = models.IntegerField()
   date_entree = models.DateField()
   date_sortie = models.DateField()
   nature_reservation = models.CharField(max_length=20, choices=NATURE_CHOICES)
   restauration_montant = models.DecimalField(max_digits=10, decimal_places=2)

   def __str__(self):
      return f"Reservation for {self.resident} at {self.hauberge}"
   

class HaubergeResident(models.Model):
   hauberge = models.ForeignKey(Hauberge, on_delete=models.CASCADE)
   resident = models.ForeignKey(Resident, on_delete=models.CASCADE)
   created_at = models.DateField(auto_now_add = True )
   def __str__(self):
      return f"{self.resident} in {self.hauberge}"