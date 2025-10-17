## 📦 Gérer ses jeux de données  

### Qu’est-ce qu’un jeu de données ?  
Un **jeu de données** correspond à un **ensemble cohérent de fichiers** (par exemple : la liste des musées de France, les festivals soutenus, les monuments historiques classés, etc.).  

Chaque jeu contient une ou plusieurs **ressources**, c’est-à-dire les fichiers eux-mêmes (formats : CSV, XLSX, JSON, GeoJSON, etc.).  

### Qu’est-ce qu’une ressource ?  
Une **ressource** est un fichier ou un lien associé à un jeu de données.  
Un même jeu peut comporter plusieurs ressources (par exemple un fichier par année, ou un fichier et une API).  

L’accès à l’interface *data.gouv.fr* permet de :  
- **modifier les informations générales** relatives au jeu (titre, description, fréquence, mots-clés) ;  
- **ajouter, remplacer ou supprimer** les ressources (fichiers) associées ;  
- **paramétrer la licence**, la visibilité et les producteurs.  

---

## 📤 Publier ou modifier une ressource  

Selon vos modalités de publication, deux situations peuvent se présenter :  

### 🧠 Cas 1 : Publication automatisée  

Si un **système de publication automatisé** est en place (via les **serveurs du ministère** ou l’infrastructure **S3 interne**),  
le dépôt des fichiers se fait **automatiquement** vers *data.gouv.fr*.  

👉 **Aucune action manuelle n’est nécessaire** sur les ressources : les fichiers sont mis à jour à intervalles réguliers selon le flux défini.  

Vous pouvez cependant **modifier à tout moment** les informations descriptives (*métadonnées*) depuis l’interface de *data.gouv.fr* :  
- titre,  
- description,  
- mots-clés (*tags*),  
- fréquence de mise à jour,  
- licence ou producteurs associés.  

Cette articulation garantit une **mise à jour fiable et continue** des données, tout en assurant une **qualité éditoriale** et une **présentation cohérente** sur *culture.data.gouv.fr*.  

---

### 🖐️ Cas 2 : Publication manuelle  

Lorsque la publication n’est **pas automatisée**, vous pouvez :  
- **déposer manuellement** le fichier via l’interface *data.gouv.fr* (méthode la plus courante) ;  
- ou **utiliser l’API data.gouv.fr** pour mettre à jour le fichier via un script automatisé léger.  

Pour mettre à jour une ressource :  
1. **Se connecter** sur [data.gouv.fr](https://www.data.gouv.fr/) ;  
2. **Ouvrir** le jeu de données concerné ;  
3. **Cliquer** sur **« Remplacer la ressource »** pour déposer la nouvelle version du fichier ;  
4. **Mettre à jour** la description ou la fréquence si nécessaire ;  
5. **Enregistrer** : la version actualisée sera automatiquement visible sur [culture.data.gouv.fr](https://culture.data.gouv.fr).  

💡 *Vérifiez la cohérence entre la description du jeu et les ressources associées avant validation.*  

---

### 📝 Bonnes pratiques  

Pour garantir la qualité, la clarté et la découvrabilité des données publiées :  

- **Rédigez une description claire et contextualisée**, accompagnée d’une **courte description** (résumé) pour faciliter la lecture rapide du contenu ;  
- **Ajoutez la fréquence de publication** (unique, annuelle, mensuelle, temps réel...) pour informer les réutilisateurs ;  
- **Ajoutez des mots-clés (tags)** pertinents pour améliorer la **recherche et la visibilité** du jeu de données sur *data.gouv.fr* et *culture.data.gouv.fr* ;  
- **Soignez les titres et les formats de fichiers** (ex. : `liste_musees_2025.csv`) pour renforcer la cohérence et la traçabilité.  

💡 *Une donnée bien décrite est une donnée mieux comprise, réutilisée et valorisée.*  


---

**Guides :**  
[1. Les plateformes](../Guides/plateformes.md) •  
[2. S’inscrire](../Guides/inscription.md) •  
[3. Publier / modifier](../Guides/publier_modifier.md) •  
[4. Accompagnement](../Guides/accompagnement_contacts.md)  

[⬆️ Retour au sommaire principal](../README.md)

