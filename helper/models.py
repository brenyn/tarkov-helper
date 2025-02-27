from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from helper import db, login_manager, app
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
  return User.query.get(int(user_id))

class User(db.Model, UserMixin):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), unique=True, nullable=False)
  email = db.Column(db.String(120), unique=False, nullable=False)
  password = db.Column(db.String(60), nullable=False)

  def get_reset_token(self, expires_sec=1800):
    s = Serializer(app.config['SECRET_KEY'], expires_sec)
    return s.dumps({'user_id':self.id}).decode('utf-8')

  @staticmethod
  def verify_reset_token(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
      user_id = s.loads(token)['user_id']
    except:
      return None
    return User.query.get(user_id)

  def __repr__(self):
    return f"User('{self.username}','{self.email}'"

class Ammo(db.Model):
  ammo_id = db.Column(db.Integer, primary_key=True)
  ammo_type = db.Column(db.String(20), unique=False, nullable=False)
  round = db.Column(db.String(20), unique=False, nullable=False)
  damage = db.Column(db.Integer, unique=False, nullable=False)
  penetration = db.Column(db.Integer, unique=False, nullable=False)
  armor_damage = db.Column(db.Integer, unique=False, nullable=False)
  frag_chance = db.Column(db.String, unique=False, nullable=False)

  def __repr__(self):
    return f"Ammo('{self.ammo_type}','{self.round}', '{self.damage}','{self.penetration}','{self.armor_damage}','{self.frag_chance}'"

class QuestModel(db.Model):
  quest_id = db.Column(db.Integer, primary_key=True)
  quest_giver = db.Column(db.String(20), unique=False, nullable=False)
  quest_title = db.Column(db.String(30), unique=False, nullable=False)
  quest_objectives = db.Column(db.String(200), unique=False, nullable=False)
  quest_rewards = db.Column(db.String(200), unique=False, nullable=False)

  def __repr__(self):
    return f"QuestModel('{self.quest_giver}',{self.quest_title}',{self.quest_objectives}',{self.quest_rewards}')"