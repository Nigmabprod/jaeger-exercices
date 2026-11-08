# Exercices Jaeger : les bases du tracing distribué

## L'application : une librairie en ligne

Deux services Python. Chacun envoie ses **traces** à Jaeger.

```
            ┌──────────────┐         ┌──────────────┐
client ───► │   frontend   │ ──────► │   backend    │ ──► base de données / banque
            │ (la vitrine) │         │ (stock, prix,│      (simulées)
            └──────────────┘         │  paiements)  │
                   │                 └──────────────┘
                   └───────── traces ───────┴──────► Jaeger  http://localhost:16686
```

### Ce qui se passe quand on **commande** (`http://localhost:8080/commande`)

1. Le **frontend** reçoit la commande du livre *Le Petit Prince*.
2. **verifier-stock** : le frontend demande au backend combien d'exemplaires il reste (`GET /stock`). Le backend lit la base de données (**lire-base-de-donnees**).
3. **obtenir-prix** : le frontend demande le prix au backend (`GET /prix`).
4. Le frontend répond au client : `{"commande": "acceptee", "livre": "Le Petit Prince", "exemplaires_en_stock": 42, "prix_htva": 20.0}`

### Ce qui se passe quand on **paie** (`http://localhost:8080/paiement`)

1. **payer-commande** : le frontend demande au backend d'encaisser le paiement (`POST /paiement`).
2. Le backend contacte la banque (**appeler-banque**).
3. Le client reçoit `{"paiement": "accepte", "montant": 24.2}`, ou une erreur.

> Dans Jaeger, **chaque étape est un span**. Les noms en gras ci-dessus sont ceux que vous verrez. Les spans nommés simplement `GET` ou `POST` sont les appels HTTP qu'un service envoie à l'autre ; ils sont créés automatiquement par OpenTelemetry.

---

## Démarrage

Prérequis : Docker et Docker Compose.

```bash
git clone https://github.com/Nigmabprod/jaeger-exercices.git
cd jaeger-exercices
docker compose up -d --build
```

- Application : http://localhost:8080
- Jaeger : http://localhost:16686

Passer 20 commandes d'un coup (chaque ligne affiche `numéro : code HTTP durée`) :
```powershell
# Windows PowerShell
1..20 | % { curl.exe -s -o NUL -w "$_ : %{http_code} %{time_total}s`n" localhost:8080/commande }
```
```bash
# Linux / macOS / Git Bash
for i in $(seq 20); do curl -s -o /dev/null -w "$i : %{http_code} %{time_total}s\n" localhost:8080/commande; done
```
Pour les paiements, remplacez `commande` par `paiement` dans la commande.

Arrêt : `docker compose down`

---

## Exercices

Les consignes se trouvent dans **[CONSIGNES.md](CONSIGNES.md)**.
