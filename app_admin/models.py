from django.db import models

# Create your models here.

class Country(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Region(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    
    
    def __str__(self):
        return self.name

class Zone(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Woreda(models.Model):
    
    name = models.CharField(max_length=255, unique=True)
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
    class Meta:
        ordering = ('name',)
    
class FieldOffice(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, null=True, blank=True)
    zone = models.ForeignKey(
        Zone, on_delete=models.CASCADE, null=True, blank=True)
    woreda = models.ForeignKey(
        Woreda, on_delete=models.CASCADE, null=True, blank=True)
    

    def __str__(self):
        return str(self.name)
    
class Portfolio_Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Portfolio_Category(models.Model):
    type = models.ForeignKey(Portfolio_Type, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name

class Approvalt_Status(models.Model):
    name = models.CharField(max_length=255)
    
    def __int__(self):
        return self.id

class Approvalf_Status(models.Model):
    name = models.CharField(max_length=255)
    
    def __int__(self):
        return self.id

class Submission_Status(models.Model):
    name = models.CharField(max_length=255)
    
    def __int__(self):
        return self.id
    
class Travel_Cost(models.Model):
    name = models.CharField(max_length=255)
    
    def __int__(self):
        return self.name
    

class Fund(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Lin_Code(models.Model):
    fund = models.ForeignKey(Fund, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    
    def __str__(self):
        return self.name
    
class Feedback_Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Feedback_Channel(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Informant_Age(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Informant_Gender(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Informed_Consent(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Informant_Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Feedback_Status(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Feedback_Response_Type(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class Feedback_Resolution(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name