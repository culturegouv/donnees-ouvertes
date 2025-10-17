# 📦 Gérer ses jeux de données  

## Jeux de données et fichiers  

### 🧭 Comprendre les termes utilisés  

Sur *data.gouv.fr*, l’interface emploie les termes **“jeu de données”** et **“fichier”**.  
Dans la documentation technique ou les échanges avec les équipes, ces termes correspondent respectivement à :  

| Terme affiché sur data.gouv.fr | Terme technique (API / code) | Définition |
|--------------------------------|-------------------------------|-------------|
| **Jeu de données** | `dataset` | Ensemble cohérent de fichiers et de métadonnées regroupés autour d’un même thème. |
| **Fichier** | `ressource` | Contenu du jeu de données : un fichier (CSV, XLSX, JSON…), une API ou un lien de téléchargement. |

> 🔍 À retenir : un *jeu de données* (dataset) regroupe plusieurs *fichiers* (ressources) et leurs descriptions.

---

### 📚 Qu’est-ce qu’un jeu de données ?  

Un **jeu de données** correspond à un **ensemble cohérent de fichiers et de métadonnées** (titre, description, producteur, mots-clés, date de publication, fréquence de mise à jour, etc.).  
C’est l’unité principale de publication sur *data.gouv.fr*.

> 🔗 [Lire la définition officielle sur guides.data.gouv.fr](https://guides.data.gouv.fr/guide-data.gouv.fr/jeux-de-donnees)

Exemples de jeux de données :  
- la **liste des musées de France**,  
- les **festivals soutenus par le ministère**,  
- les **monuments historiques classés**.  

Chaque jeu de données contient une ou plusieurs ressources (fichiers, liens, API, etc.).

---

### 📁 Qu’est-ce qu’un fichier (ou ressource) ?  

Une **ressource** est un **fichier ou un lien associé à un jeu de données**.  
Elle contient les données elles-mêmes et peut prendre plusieurs formes :  

- un fichier au format **CSV**, **XLSX**, **JSON**, **GeoJSON** ;  
- une **API** donnant accès à des données actualisées ;  
- ou un **lien** vers une autre source d’information.

Un même jeu peut comporter plusieurs ressources — par exemple, un fichier par année, ou un fichier et son API associée.

---

### 🧰 Que permet l’interface *data.gouv.fr* ?  

Depuis l’espace d’administration, vous pouvez :  
- **modifier les informations générales** du jeu (titre, description, fréquence, mots-clés, producteur, licence) ;  
- **ajouter, remplacer ou supprimer des fichiers** associés au jeu ;  
- **paramétrer la visibilité** (publique ou privée).  

![Interface de gestion d’un jeu de données sur data.gouv.fr](https://github.com/culturegouv/donnees-ouvertes/blob/main/librairie-image/interface_dataset.png?raw=true)

> Exemple : interface de gestion d’un jeu de données sur *data.gouv.fr* permettant d’ajouter, remplacer ou modifier des fichiers.

---

## 📤 Publier ou modifier un fichier  

Selon vos modalités de publication, deux situations peuvent se présenter :  

### 🧠 Cas 1 : Publication automatisée  

Si un **système de publication automatisé** est en place (via les **serveurs du ministère** ou l’infrastructure **S3 interne**),  
le dépôt des fichiers se fait **automatiquement** vers *data.gouv.fr*.  

👉 **Aucune action manuelle n’est nécessaire** sur les fichiers : ils sont mis à jour à intervalles réguliers selon le flux défini.  

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
- **déposer manuellement** un fichier via l’interface *data.gouv.fr* (méthode la plus courante) ;  
- ou **utiliser l’API data.gouv.fr** pour mettre à jour le fichier via un script automatisé léger.  

Pour mettre à jour un fichier :  
1. **Se connecter** sur [data.gouv.fr](https://www.data.gouv.fr/) ;  
2. **Ouvrir** le jeu de données concerné ;  
3. **Cliquer** sur **« Remplacer la ressource »** pour déposer la nouvelle version du fichier ;  
4. **Mettre à jour** la description ou la fréquence si nécessaire ;  
5. **Enregistrer** : la version actualisée sera automatiquement visible sur [culture.data.gouv.fr](https://culture.data.gouv.fr).  

💡 *Vérifiez la cohérence entre la description du jeu et les fichiers associés avant validation.*  

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
