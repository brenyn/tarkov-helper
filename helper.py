from flask import Flask, render_template
app = Flask(__name__)

ammoTypes = [
  {
    'type':'762x39',
    'rounds':
      [
        {
          'round_name':'HP',
          'damage':87,
          'penetration':15
        },
        {
          'round_name':'US',
          'damage':56,
          'penetration':29
        }
      ]
  },
  {
    'type':'762x51',
    'rounds':
      [
        {
          'round_name':'HP',
          'damage':87,
          'penetration':15
        },
        {
          'round_name':'US',
          'damage':56,
          'penetration':29
        }
      ]
  },
]

# for ammo in ammoTypes:
# 	print(ammo['type'])
# 	for i in range(len(ammo['rounds'])):
# 		print(ammo['rounds'][i]['round_name'])

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/ammo")
def ammo():
    return render_template('ammo.html', ammoTypes=ammoTypes)

# run server in debug mode if script is run from command line
if __name__ == '__main__':
  app.run(debug=True)