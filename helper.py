from flask import Flask, render_template
app = Flask(__name__)

@app.route("/")
@app.route("/index.html")
def home():
  return render_template('index.html')

@app.route("/ammo.html")
def ammo():
    return render_template('ammo.html')

# run server in debug mode if script is run from command line
if __name__ == '__main__':
  app.run(debug=True)