"""Service 'backend' : gère le stock, les prix et les paiements de la librairie."""
import itertools
import random
import time

from flask import Flask
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer("backend")

# Compteurs d'appels (pour rendre les problèmes reproductibles)
lectures_stock = itertools.count(1)
appels_banque = itertools.count(1)


@app.get("/stock")
def stock():
    # On lit le nombre d'exemplaires dans la base de données
    with tracer.start_as_current_span("lire-base-de-donnees") as span:
        span.set_attribute("db.table", "livres")
        # ...une lecture sur cinq est très lente
        if next(lectures_stock) % 5 == 0:
            time.sleep(1.5)
        else:
            time.sleep(random.uniform(0.01, 0.05))
    return {"livre": "Le Petit Prince", "exemplaires": 42}


@app.get("/prix")
def prix():
    time.sleep(random.uniform(0.01, 0.03))
    return {"prix_htva": 20.0}


@app.post("/paiement")
def paiement():
    # On demande à la banque d'encaisser le montant
    with tracer.start_as_current_span("appeler-banque") as span:
        span.set_attribute("paiement.montant", 24.2)
        time.sleep(random.uniform(0.02, 0.08))
        # ...un appel sur trois échoue
        if next(appels_banque) % 3 == 0:
            raise RuntimeError("Banque injoignable (timeout)")
    return {"paiement": "accepte", "montant": 24.2}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
