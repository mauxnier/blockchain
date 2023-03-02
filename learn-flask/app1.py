import flask
app = flask.Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def home():
    return "<h1>Annuaire Internet</h1><p>Ce site est le prototype d’une API mettant à disposition des données sur les employés d’une entreprise.</p>"

app.run()
