class Config:
  app.config['SECRET_KEY'] = '2a9421a498f13bd18ce8cc0851dd7413'
  app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
  app.config['MAIL_SERVER'] = 'smtp.gmail.com'
  app.config['MAIL_PORT'] = 465
  app.config['MAIL_USE_SSL'] = True
  app.config['MAIL_USERNAME'] = os.environ.get('HELPER_MAIL_USERNAME')
  app.config['MAIL_PASSWORD'] = os.environ.get('HELPER_MAIL_PASSWORD')
