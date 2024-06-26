import csv
from datetime import datetime
from django.core.management.base import BaseCommand
from homicides_api.models import *

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    def handle(self, *args, **kwargs):
        self.load_victims()
        self.load_locations()
        self.load_dispositions()
        self.load_homicides()

    def load_victims(self):
        with open('csv_files/victims.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Victim.objects.create(
                    race=row['victim_race'],
                    age=row['victim_age'],
                    sex=row['victim_sex']
                )

    def load_locations(self):
        with open('csv_files/locations.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Location.objects.create(
                    city=row['city'],
                    state=row['state']
                )

    def load_dispositions(self):
        with open('csv_files/dispositions.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                Disposition.objects.create(
                    disposition=row['disposition']
                )

    def load_homicides(self):
        with open('csv_files/homicides.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                # Find the related foreign key objects
                victim = Victim.objects.get(id=row['victim_id'])
                location = Location.objects.get(id=row['location_id'])
                disposition = Disposition.objects.get(id=row['disposition_id'])
                
                # Create the Homicide object with the foreign keys
                Homicide.objects.create(
                    date=datetime.strptime(row['reported_date'], '%Y-%m-%d').date(),
                    victim=victim,
                    location=location,
                    disposition=disposition
                )