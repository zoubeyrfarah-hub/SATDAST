import os
from flask import Flask, request, make_response
from markupsafe import escape

app = Flask(__name__)

# 1. Remédiation SAST : Ne jamais coder de secrets en dur.
# On utilise les variables d'environnement (avec une valeur par défaut inoffensive si besoin).
DB_PASSWORD = os.environ.get("DB_PASSWORD", "default_safe_value")

@app.route('/')
def home():
    return "Bienvenue sur l'environnement sécurisé DevSecOps !"

# 2. Remédiation SAST & DAST : Prévention de la faille Cross-Site Scripting (XSS)
@app.route('/bonjour')
def bonjour():
    nom = request.args.get('nom', 'Invité')
    # L'utilisation de escape() convertit les caractères spéciaux (comme <, >, &) en entités HTML.
    # Ainsi, un script malveillant sera affiché comme du texte au lieu d'être exécuté par le navigateur.
    nom_securise = escape(nom)
    return f"<h1>Bonjour {nom_securise}</h1><p>Ceci est un test de sécurité réussi.</p>"

# 3. Remédiation DAST : Ajout des en-têtes de sécurité HTTP
@app.after_request
def add_security_headers(response):
    # Empêche le navigateur de deviner le type de contenu (MIME sniffing)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Empêche l'application d'être incluse dans un iframe (Clickjacking)
    response.headers['X-Frame-Options'] = 'DENY'
    # Politique stricte limitant le chargement des ressources au domaine actuel
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    return response

if __name__ == '__main__':
    # 4. Remédiation : Désactivation du mode debug (qui expose des informations sensibles en cas d'erreur)
    app.run(host='0.0.0.0', port=5000, debug=False)
