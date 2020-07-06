from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
  return "<h1>Home page</h1>"

@app.route("/about")
def about():
    return "<h1>About Page</h1>"

# run server in debug mode if script is run from command line
if __name__ == '__main__':
  app.run(debug=True)