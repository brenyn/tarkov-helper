import csv
from helper import db
from helper.models import Ammo

db.drop_all()
db.create_all()

with open ('helper/ammo-csv.csv') as ammocsv:
  reader = csv.DictReader(ammocsv)
  ammotypes = list(reader)

for ammo in ammotypes:
  db_ammo = Ammo(ammo_type=ammo['Ammo Type'], round=ammo['Round'],damage=int(ammo['Damage']), penetration=int(ammo['Pen Value']),armor_damage=int(ammo['Armor Damage %']), frag_chance=ammo['Frag. Chance*'])
  db.session.add(db_ammo)
  db.session.commit()

ammoTypes= []
calibers=['12 Gauge Shot',
  '12 Gauge Slugs',
  '20 Gauge',
  '9x18mm',
  '7.62x25mm',
  '9x19mm',
  '0.45',
  '9x21mm',
  '5.7x28 mm',
  '4.6x30 mm',
  '9x39mm',
  '0.366',
  '5.45x39 mm',
  '5.56x45 mm',
  '7.62x51 mm',
  '7.62x54R',
  '12.7x55 mm',]
for caliber in calibers:
  print(caliber)
#   append dictionary to ammoTypes list w/ keys 'type': caliber, 'rounds':[]
#   query by caliber
#   append each round of caliber to list of dictionaries containing round name/stats