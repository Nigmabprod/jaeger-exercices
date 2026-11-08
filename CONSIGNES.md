# Consignes : exercices Jaeger

Avant de commencer, lancez l'application et lisez la section « L'application » du [README](README.md) : elle explique ce qui se passe lors d'une commande et d'un paiement.

Commandes utiles (PowerShell) :
```powershell
1..20 | % { curl.exe -s -o NUL -w "$_ : %{http_code} %{time_total}s`n" localhost:8080/commande }
1..10 | % { curl.exe -s -o NUL -w "$_ : %{http_code}`n" localhost:8080/paiement }
```

---

## Exercice 1 : lire une trace

1. Ouvrez http://localhost:8080/commande dans votre navigateur.
2. Dans Jaeger, choisissez le service `frontend` et cliquez sur **Find Traces**. Ouvrez la trace `frontend: GET /commande`.

**Questions**
- Combien de **services** et de **spans** compte la trace ?
- Retrouvez dans la trace les étapes décrites dans le README, section « Ce qui se passe quand on commande ». Le stock et le prix sont-ils demandés **en même temps**, ou l'un après l'autre ?
- Sous `verifier-stock`, il y a un span `GET` dans le frontend, puis un span `GET /stock` dans le backend. Pourquoi deux spans pour un seul appel ?

## Exercice 2 : pourquoi certaines commandes sont lentes ?

1. Passez 20 commandes avec la commande donnée en haut de cette page.
2. Dans Jaeger, triez avec **Longest First**, ou filtrez avec **Min Duration** = `1s`.

**Questions**
- Combien de commandes sont lentes ?
- Quelle **étape** est responsable ? Dans quel **service** ?

## Exercice 3 : pourquoi certains paiements échouent ?

1. Faites 10 paiements avec la commande donnée en haut de cette page.
2. Dans Jaeger, recherchez avec **Tags** = `error=true`.

**Questions**
- Dans quel span l'erreur **naît-elle** ? Comment remonte-t-elle jusqu'au client ?
- Quel est le **message d'erreur** ? (Indice : regardez les *Logs/Events* du span.)
- Quel code HTTP le client reçoit-il ?

## Exercice 4 : ajouter votre propre étape

Le backend calcule seulement un prix hors TVA. Dans `app/backend.py`, dans la fonction `prix()`, ajoutez une étape **`calculer-tva`** :

- elle porte l'attribut `tva.taux` = `0.21` ;
- elle porte l'attribut `prix.tvac` (le prix TVA comprise).

Inspirez-vous de `lire-base-de-donnees`, plus haut dans le même fichier :
```python
with tracer.start_as_current_span("nom-de-l-etape") as span:
    span.set_attribute("cle", valeur)
```

Appliquez la modification avec `docker compose restart backend`, passez une commande, puis retrouvez votre étape dans Jaeger.

**Question**
- Où apparaît `calculer-tva` dans la trace ? Qui est son parent ?

## Exercice 5 (bonus) : vue d'ensemble

- Onglet **System Architecture** : quelles dépendances entre services Jaeger affiche-t-il ?
- Sélectionnez une commande rapide et une commande lente, puis cliquez sur **Compare**. Qu'est-ce qui diffère ?
