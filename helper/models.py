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
  ammotype = db.Column(db.String(20), unique=False, nullable=False)
  round = db.Column(db.String(20), unique=False, nullable=False)
  damage = db.Column(db.Integer, unique=False, nullable=False)
  penetration = db.Column(db.Integer, unique=False, nullable=False)
  armor_damage = db.Column(db.Integer, unique=False, nullable=False)
  frag_chance = db.Column(db.Integer, unique=False, nullable=False)