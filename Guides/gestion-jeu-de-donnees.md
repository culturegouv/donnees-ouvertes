# Publier ses données sur data.gouv.fr
## Mode d’emploi à destination des agents et opérateurs du ministère de la Culture

### 🌐 1. Comprendre les plateformes

#### data.gouv.fr

C’est la plateforme nationale d’ouverture des données publiques.
Elle permet :

* de créer, gérer et mettre à jour les jeux de données du ministère ;
* d’en décrire le contenu, le contexte et la fréquence de publication ;
* de déposer les fichiers associés (appelés « ressources ») ou d’automatiser leur alimentation.

#### culture.data.gouv.fr

C’est la vitrine thématique des données culturelles ouvertes.
Elle permet :

* de visualiser et explorer les jeux publiés par le ministère et ses opérateurs ;
* d’offrir une interface simplifiée pour les réutilisateurs (chercheurs, journalistes, développeurs, citoyens) ;
* de valoriser les politiques culturelles et les initiatives territoriales.

👉 En résumé :

* data.gouv.fr = la gestion et la publication des jeux de données ;
* culture.data.gouv.fr = la visualisation et la valorisation des données culturelles.

### 👤 2. Obtenir les accès éditeur sur data.gouv.fr

Créez votre compte via ce lien : S’enregistrer sur data.gouv.fr

Depuis la page “Organisation du ministère de la Culture”, cliquez sur « Demander à rejoindre l’organisation » ;

L’équipe du Département des politiques numériques culturelles (DPNC) validera ensuite votre profil en tant qu’éditeur ;

Une fois validé, vous pourrez :

* créer de nouveaux jeux de données ;
* modifier ou compléter les métadonnées (titre, description, mots-clés, fréquence de publication) ;
* ajouter ou remplacer les fichiers associés.

### 📦 3. Gérer ses jeux de données
Qu’est-ce qu’un jeu de données ?

Un jeu de données correspond à un ensemble cohérent de fichiers (par exemple : la liste des musées de France, les festivals soutenus, les monuments historiques classés, etc.).

Chaque jeu contient une ou plusieurs ressources, c’est-à-dire les fichiers eux-mêmes (formats : CSV, XLSX, JSON, GeoJSON, etc.).

Qu’est-ce qu’une ressource ?

Une ressource est un fichier ou un lien associé à un jeu de données.
Un même jeu peut comporter plusieurs ressources (par exemple un fichier par année, ou un fichier et une API).

L’accès à l’interface data.gouv.fr permet de :

* modifier les informations générales relatives au jeu (titre, description, fréquence, mots-clés) ;
* ajouter, remplacer ou supprimer les ressources (fichiers) associées ;
* paramétrer la licence, la visibilité et les producteurs.

### 📤 4. Publication d’une ressource

Lors de la mise à jour ou de la création d’un jeu de données, deux cas de figure se présentent selon les modalités de publication mises en place.

#### Cas 1 : Publication automatisée

Si un système de publication automatisé est en place (via les serveurs du ministère ou l’infrastructure S3 interne),
le dépôt des fichiers se fait automatiquement vers data.gouv.fr.

👉 Aucune action manuelle n’est nécessaire sur les ressources : les fichiers sont mis à jour à intervalles réguliers selon le flux défini.

Le gestionnaire du jeu de données conserve toutefois la possibilité de modifier les informations descriptives (métadonnées) directement depuis l’interface de data.gouv.fr :

* titre,
* description,
* mots-clés (tags),
* fréquence de mise à jour,
* licence ou producteurs associés.

Cette articulation garantit une mise à jour fiable et continue des données, tout en maintenant une qualité éditoriale et une cohérence de présentation sur culture.data.gouv.fr.

#### 🖐️ Cas 2 : Publication manuelle

Lorsque la publication n’est pas automatisée, vous disposez de deux options :

Déposer manuellement le fichier directement via l’interface data.gouv.fr (méthode la plus courante) ;

ou utiliser l’API data.gouv.fr pour mettre à jour le fichier via un script ou un outil automatisé léger.

À chaque mise à jour, vous devez :

* Vous connecter sur data.gouv.fr ;
* Ouvrir le jeu de données concerné ;
* Cliquer sur « Remplacer la ressource » pour déposer la nouvelle version du fichier ;
* Mettre à jour la description ou la fréquence si nécessaire ;
* Enregistrer les modifications.

Les changements seront automatiquement répercutés sur la plateforme culture.data.gouv.fr.

##### 📝 Bonnes pratiques

Pour garantir la qualité, la clarté et la découvrabilité des données publiées :

* Rédigez une description claire et contextualisée, accompagnée d’une courte description (résumé) pour faciliter la lecture rapide du contenu ;
* Ajoutez la fréquence de publication (unique, annuelle, mensuelle, temps réel...) afin d’informer les réutilisateurs sur le rythme des mises à jour ;
* Ajoutez des mots-clés (tags) pertinents pour améliorer la recherche et la découvrabilité du jeu de données sur culture.data.gouv.fr
 et data.gouv.fr ;

Soignez les titres et les formats de fichiers (ex. : liste_musees_2025.csv) pour renforcer la cohérence et la traçabilité des publications.

💡 Une donnée bien décrite est une donnée mieux comprise, réutilisée et valorisée.

### 🧭 5. En cas de mise à jour
Se connecter et mettre à jour une ressource

Lorsque vous modifiez un jeu ou un fichier :

* Se connecter sur data.gouv.fr
 ;
* Ouvrir le jeu de données concerné ;
* Cliquer sur « Remplacer la ressource » pour mettre à jour le fichier ;
* Mettre à jour la description si nécessaire (titre, fréquence, mots-clés, etc.) ;
* Enregistrer : la version actualisée sera automatiquement visible sur culture.data.gouv.fr
.

💡 Pensez à vérifier la cohérence entre la description du jeu et les ressources associées avant validation.

### 🧩 6. Accompagnement et contacts

Le Département des politiques numériques culturelles (DPNC) du Service du numérique vous accompagne dans :

* la prise en main de l’interface data.gouv.fr ;

* la structuration et l’enrichissement des métadonnées ;

* la mise en place de publications automatisées via les infrastructures ministérielles ;

* la valorisation et la visibilité des jeux de données sur culture.data.gouv.fr.


📧 Contact : circulation.donnees@culture.gouv.fr

📚 Ressources : guide pratique, tutoriels, modèles de fiches et sessions de formation internes.
