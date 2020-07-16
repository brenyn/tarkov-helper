import csv

with open ('helper/ammo-csv.csv') as ammocsv:
  reader = csv.DictReader(ammocsv)
  ammotypes = list(reader)