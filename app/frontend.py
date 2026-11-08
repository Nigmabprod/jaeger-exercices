"""Service 'frontend' : la vitrine de la librairie.

Il reçoit les requêtes des clients et demande au backend ce dont il a besoin.
"""
import requests
from flask import Flask
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer("frontend")
BACKEND = "http://backend:8081"


@app.get("/")
def accueil():
    return (
        "Librairie en ligne\n"
        "  /commande  -> commander le livre 'Le Petit Prince'\n"
        "  /paiement  -> payer la commande\n"
    )


@app.get("/commande")
def commande():
    # Étape 1 : demander au backend s'il reste des exemplaires
    with tracer.start_as_current_span("verifier-stock"):
        stock = requests.get(f"{BACKEND}/stock", timeout=10).json()

    # Étape 2 : demander au backend le prix du livre
    with tracer.start_as_current_span("obtenir-prix"):
        prix = requests.get(f"{BACKEND}/prix", timeout=10).json()

    return {
        "commande": "acceptee",
        "livre": stock["livre"],
        "exemplaires_en_stock": stock["exemplaires"],
        "prix_htva": prix["prix_htva"],
    }


@app.get("/paiement")
def paiement():
    # Demander au backend d'encaisser le paiement
    with tracer.start_as_current_span("payer-commande"):
        r = requests.post(f"{BACKEND}/paiement", timeout=10)
        r.raise_for_status()
    return r.json()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
