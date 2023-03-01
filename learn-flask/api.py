# Import de bibliothèques
import flask
from flask import request, jsonify
# Création de l'objet Flask
app = flask.Flask(__name__)
# Lancement du Débogueur
app.config["DEBUG"] = True
# Quelques données tests pour l’annuaire sous la forme d’une liste de dictionnaires
employees = [
    {'id': 0,
     'Nom': 'Dupont',
     'Prénom': 'Jean',
     'Fonction': 'Développeur',
     'Ancienneté': '5'},
    {'id': 1,
     'Nom': 'Durand',
     'Prénom': 'Elodie',
     'Fonction': 'Directrice Commerciale',
     'Ancienneté': '4'},
    {'id': 2,
     'Nom': 'Lucas',
     'Prénom': 'Jérémie',
     'Fonction': 'DRH',
     'Ancienneté': '4'}
]

@app.route('/', methods=['GET'])
def home():
    return '''<h1>Annuaire Internet</h1>
    <p>Ce site est le prototype d’une API mettant à disposition des données sur les
    employés d’une entreprise.</p>'''
# Route permettant de récupérer toutes les données de l’annuaire
@app.route('/api/v1/resources/employees/all', methods=['GET'])
def api_all():
    return jsonify(employees)
