import requests
from bs4 import BeautifulSoup
from datetime import date
import csv

table_classes=['Prapor-content',
'Therapist-content',
'Skier-content',
'Peacekeeper-content',
'Mechanic-content',
'Ragman-content',
'Jaeger-content',
'Fence-content',]

class Quest:
  def __init__(self, quest, objectives, rewards):
    self.quest = quest
    self.objectives = objectives
    self.rewards = rewards

r = requests.get('https://escapefromtarkov.gamepedia.com/Quests')
soup = BeautifulSoup(r.text, 'html.parser')

for table_class in table_classes:
  table = soup.find("table",{"class":table_class})
  quest_giver = table.th.a.text.strip()
  table_quests = table.find_all('tr')
  del table_quests[0:2]
  for current_quest in table_quests:
    quest_title = current_quest.find("th")
    print(quest_title.text.strip())
    quest_cells = current_quest.find_all("td")
    quest_objectives = quest_cells[0].text.strip()
    print(quest_objectives)
    quest_rewards = quest_cells[1].text.strip()
    print(quest_rewards)