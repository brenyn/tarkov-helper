from flask import Flask, render_template
app = Flask(__name__)

ammoTypes= [
  {'762x39':
    (
      {
      'round': 'HP',
      'damage': 87,
      'penetration':15
      },
      {
        'round': 'US',
        'damage':56,
        'penetration':29
      }
    )
  },
  {'762x51':
    (
      {
      'round': 'M62',
      'damage': 87,
      'penetration':15
      },
      {
        'round': 'M61',
        'damage':56,
        'penetration':29
      }
    )
  },
]


# for ammo in ammoTypes:
# 	for round in ammo.items():
# 		print(round[1][0]['round'])

@app.route("/")
def home():
  return render_template('index.html')

@app.route("/ammo")
def ammo():
    return render_template('ammo.html', ammoTypes=ammoTypes)

# run server in debug mode if script is run from command line
if __name__ == '__main__':
  app.run(debug=True)