import os
from flask import Flask, request, abort
from markupsafe import escape

app = Flask(__name__)

# Jeton secret attendu pour accéder à l'administration
# (Dans la vraie vie, cela serait géré via une base de données ou un fournisseur d'identité)
EXPECTED_TOKEN = "Bearer token_etudiant_123"

@app.route('/')
def home():
    return "Bienvenue sur l'environnement DevSecOps !"

@app.route('/bonjour')
def bonjour():
    nom = request.args.get('nom', 'Invité')
    nom_securise = escape(nom) # Route sécurisée
    return f"<h1>Bonjour {nom_securise}</h1>"

# --- NOUVELLE ZONE PROTÉGÉE ---
@app.route('/admin')
def admin_panel():
    # 1. Vérification des privilèges (Authentification)
    auth_header = request.headers.get('Authorization')
    
    if auth_header != EXPECTED_TOKEN:
        # Rejet de la requête si le scanner ou l'utilisateur n'a pas le bon jeton
        abort(401, description="Accès refusé : Jeton d'authentification manquant ou invalide.")
    
    # 2. Zone vulnérable (Accessible uniquement après authentification)
    # Nous omettons volontairement la fonction escape() ici pour créer une faille XSS
    action = request.args.get('action', 'affichage_dashboard')
    
    return f"<h1>Administration</h1><p>Action exécutée : {action}</p><p><i>Données confidentielles du serveur...</i></p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
