import csv, json
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