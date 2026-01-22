# Message d'erreur

## Page dataset - ressource : "L'aperçu de ce fichier n'a pas pu être chargé."
<img width="1253" height="335" alt="image" src="https://github.com/user-attachments/assets/f1c5a88f-b1c0-4bb3-9ac4-07104d37a90c" />

### Description du problème
Un message d'erreur s'affiche lorsque vous essayez de prévisualiser un fichier dataset :
"L'aperçu de ce fichier n'a pas pu être chargé."

Cette erreur est liée à un dysfonctionnement de l'API Tabular, qui retourne le message suivant :
"La ressource a été supprimée."

### Note importante 
Ce message est erroné. La ressource n'a pas été supprimée et reste disponible.

### Vérification / reproduction
https://tabular-api.data.gouv.fr/api/resources/[ID RESSOURCE]
### Statut actuel
Problème identifié : L'erreur provient d'une incohérence entre l'API et le système de gestion des ressources.
### Actions en cours :
Une investigation technique est en cours pour déterminer la cause exacte du dysfonctionnement.
Une correction est prévue pour rétablir l'affichage des aperçus des fichiers concernés.
Échéance estimée : Une résolution est attendue sous 48 à 72 heures (sous réserve de confirmation technique).

### Solutions temporaires
En attendant la résolution du problème, voici quelques alternatives pour accéder aux données :

* Télécharger le fichier :
Cliquez sur le bouton de téléchargement (si disponible) pour récupérer le fichier en local et l'ouvrir avec un outil adapté (LibreOffice, etc.).

