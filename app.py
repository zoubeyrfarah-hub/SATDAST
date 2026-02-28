from flask import Flask, request

app = Flask(__name__)

# Vulnérabilité SAST : Identifiants codés en dur
DB_PASSWORD = "super_secret_password_123!"

@app.route('/')
def home():
    return "Bienvenue sur l'environnement de test DevSecOps en Python !"

# Vulnérabilité SAST/DAST : Reflected XSS
@app.route('/bonjour')
def bonjour():
    nom = request.args.get('nom', 'Invité')
    # L'entrée n'est pas sécurisée (échappée), permettant l'injection de code HTML/JS
    return f"<h1>Bonjour {nom}</h1><p>Ceci est un test de sécurité.</p>"

if __name__ == '__main__':
    # Vulnérabilité : Exécution de l'application avec le mode debug activé
    app.run(host='0.0.0.0', port=5000, debug=True)