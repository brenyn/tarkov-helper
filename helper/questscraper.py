import requests
from bs4 import BeautifulSoup
from datetime import date
from helper import db
from helper.models import QuestModel

QuestModel.__table__.drop()
db.create_all()

table_classes=['Prapor-content',
'Therapist-content',
'Skier-content',
'Peacekeeper-content',
'Mechanic-content',
'Ragman-content',
'Jaeger-content',
'Fence-content',]

# class Quest:
#   def __init__(self, giver ,quest, objectives, rewards):
#     self.giver = giver
#     self.quest = quest
#     self.objectives = objectives
#     self.rewards = rewards

r = requests.get('https://escapefromtarkov.gamepedia.com/Quests')
soup = BeautifulSoup(r.text, 'html.parser')

for table_class in table_classes:
  table = soup.find("table",{"class":table_class})
  quest_giver = table.th.a.text.strip()
  table_quests = table.find_all('tr')
  del table_quests[0:2]
  for current_quest in table_quests:
    quest_title = current_quest.find("th").text.strip()
    quest_cells = current_quest.find_all("td")
    quest_objectives = quest_cells[0].text.strip()
    quest_rewards = quest_cells[1].text.strip()
    db_quest = QuestModel(quest_giver=table.th.a.text.strip(), quest_title=quest_title, quest_objectives=quest_objectives,quest_rewards=quest_rewards)
    db.session.add(db_quest)
    db.session.commit()