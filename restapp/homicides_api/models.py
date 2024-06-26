from django.db import models

class Victim(models.Model):
    RACE_CHOICES = [
        ('White', 'White'),
        ('Asian', 'Asian'),
        ('Black', 'Black'),
        ('Hispanic', 'Hispanic')
    ]

    SEX_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]
    race = models.CharField(max_length=256, choices=RACE_CHOICES, null=False, blank=False)
    age = models.IntegerField(null=False, blank=True)
    sex = models.CharField(max_length=20, choices=SEX_CHOICES, null=False, blank=False)

class Location(models.Model):
    city = models.CharField(max_length=256, null=False, blank=False)
    state = models.CharField(max_length=256, null=False, blank=False)

class Disposition(models.Model):
    disposition = models.CharField(max_length=256, null=False, blank=False)

class Homicide(models.Model):
    date = models.DateField(auto_now=False, auto_now_add=False)
    victim = models.ForeignKey(Victim, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    disposition = models.ForeignKey(Disposition, on_delete=models.CASCADE)
    class Meta:
        ordering = ['id']