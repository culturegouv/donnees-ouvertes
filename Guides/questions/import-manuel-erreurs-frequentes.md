# Import manuel d’une ressource sur data.gouv : erreurs fréquentes (CSV, codes, SIRET)

Cette fiche recense les erreurs les plus courantes lors de l’import manuel d’une ressource (fichier) sur data.gouv.fr, et les bonnes pratiques associées.

## 1) Privilégier le format CSV
- Utiliser **CSV** (format ouvert, non propriétaire).

## 2) Utiliser le code commune INSEE (plutôt que le code postal)
- Pour les référencements territoriaux, privilégier le **code commune INSEE** plutôt que le **code postal**.  
  Référence INSEE : https://www.insee.fr/fr/information/7766585

## 3) Si le code postal est utilisé (non recommandé)
- Dans Excel, définir le format de cellule :
  - **Format de cellule** → **Spécial** → **Code postal**
- Objectif : éviter la perte des **zéros initiaux** (ex. `06000` transformé en `6000`).

## 4) SIRET (14 chiffres)
- Dans Excel, définir le format de cellule :
  - **Format de cellule** → **Personnalisé**
  - Masque : `00000000000000` (14 zéros)
- Objectif : conserver les **14 chiffres** et les **zéros initiaux**.
