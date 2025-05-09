### API Commandes - Documentation

#### Contexte
L'API Commandes gère les informations de commande, incluant la création, mise à jour, et suppression de commandes. Elle interagit avec les API Clients et Produits pour récupérer des informations client et produit, et utilise RabbitMQ pour une communication asynchrone entre services.

#### Prérequis
- **Python 3.9+**
- **Docker** et **Docker Compose** installés
- **RabbitMQ** en cours d'exécution avec le réseau Docker partagé `backend` (se référer à la [documentation](https://github.com/Cortexico/MSPR-RabbitMQ))
- Fichier `.env` correctement configuré avec les variables suivantes :

```plaintext
POSTGRES_USER=orders
POSTGRES_PASSWORD=apiOrders
POSTGRES_DB=orders_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

API_HOST=0.0.0.0
API_PORT=8002

RABBITMQ_HOST=rabbitmq
RABBITMQ_PORT=5672
RABBITMQ_USER=guest
RABBITMQ_PASSWORD=guest
```

#### Instructions de démarrage
#### **1. Cloner le dépôt de l'API Commandes** :
   ```bash
   git clone https://github.com/Cortexico/MSPR-API-Commandes.git
   ```
#### **2. Créer le réseau Docker partagé** (si non existant) :
   ```bash
   docker network create backend
   ```
#### **3. Créer un Environnement Virtuel**

Il est recommandé d'utiliser un environnement virtuel pour isoler les dépendances.

- **Sur Windows :**
  Création de l'environnement virtuel:
   ```bash
   python -m venv venv
   ```
  
  Lancement de l'environnement virtuel: 
   ```bash
   venv\Scripts\activate
   ```

- **Sur macOS/Linux :**

   Création de l'environnement virtuel:
   ```bash
   python3 -m venv venv
   ```
   
   Lancement de l'environnement virtuel:
   ```bash
   source venv\Scripts\activate
   ```

#### **4. Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```
#### **5. Lancer l’API avec Docker Compose** :
   ```bash
   docker-compose up --build
   ```
   - Cette commande va construire les images Docker et lancer les services définis dans `docker-compose.yml`, y compris la base de données PostgreSQL.
   
#### **6. Pour arrêter et supprimer les volumes Docker** (si nécessaire) :
   ```bash
   docker-compose down -v
   ```

#### **Sans Docker**

**1. Lancer la Base de Données PostgreSQL**

- Assurez-vous que PostgreSQL est installé et en cours d'exécution.
- Créez une base de données et un utilisateur correspondant aux variables d'environnement.

**2. Lancer l'API**

```bash
uvicorn app.main:app --host ${API_HOST} --port ${API_PORT}
```

#### **Accès à la Documentation de l'API**

- Une fois l'API lancée, accédez à la documentation interactive :

  ```
  http://localhost:8002/docs
  ```

#### Documentation technique de l'API

##### Endpoints principaux
- **GET /orders** : Récupère la liste des commandes.
  - **Réponse** : JSON array contenant les informations de chaque commande.
  
- **POST /orders** : Crée une nouvelle commande.
  - **Corps** : JSON contenant `client_id`, `product_id`, `quantity`.
  - **Réponse** : Confirmation de création avec les détails de la commande ajoutée.
  
- **GET /orders/{id}** : Récupère les détails d’une commande spécifique.
  - **Paramètre** : `id` de la commande.
  - **Réponse** : Détails de la commande en JSON.
  
- **PUT /orders/{id}** : Met à jour les informations d’une commande.
  - **Corps** : JSON avec les champs à mettre à jour (ex. `quantity`).
  - **Réponse** : Détails mis à jour de la commande.
  
- **DELETE /orders/{id}** : Supprime une commande.
  - **Paramètre** : `id` de la commande.
  - **Réponse** : Confirmation de suppression.

##### Services RabbitMQ
L'API utilise RabbitMQ pour publier et consommer des messages relatifs aux commandes.

- **Publisher** : Envoie des notifications lors de la création ou modification de commandes.
- **Consumer** : Reçoit des messages des autres API (Clients et Produits) pour vérifier les informations client et produit.

### Documentation CI/CD - GitHub Actions

#### Contexte
L'API Commandes intègre un pipeline CI/CD via GitHub Actions pour automatiser les tests et les vérifications de code, garantissant ainsi la fiabilité et la qualité du code avant chaque intégration. Ce pipeline est déclenché par des `push` et `pull requests` sur les branches du dépôt.

#### Configuration GitHub Actions
Le fichier de workflow `.github/workflows/ci.yml` contient les étapes principales pour automatiser l’intégration continue :

1. **Déclencheur** : Le pipeline CI/CD s’exécute à chaque `push` ou `pull request` vers la branche principale, ainsi que sur toute nouvelle branche.
2. **Environnement de test** : Utilise une base de données PostgreSQL dédiée pour les tests, avec un ensemble de variables d’environnement configurées dans `ci.yml`.

#### Étapes du Workflow CI/CD

1. **Configurer l'environnement** :
   - Installe les dépendances listées dans `requirements.txt`.
   - Configure la base de données de test PostgreSQL et utilise des variables d'environnement pour simuler l’environnement de production.

2. **Lancer les tests unitaires** :
   - Les tests unitaires se trouvent dans le répertoire `tests/` et sont exécutés avec `pytest` pour valider le comportement de chaque endpoint.
   - Tests inclus dans `tests/test_orders.py` :
     - `test_create_order` : Vérifie la création d’une commande.
     - `test_get_order` et `test_get_nonexistent_order` : Valident les opérations de récupération.
     - `test_update_order` : Vérifie la mise à jour d'une commande.
     - `test_delete_order` : Vérifie la suppression d'une commande.
     - `test_create_order_with_invalid_data` : Teste la validation des données d'entrée.
     
3. **Vérifications de code** :
   - Le pipeline utilise `flake8` pour analyser le style du code et garantir la qualité.
   - Tout échec déclenche un arrêt du workflow, assurant que seules les modifications conformes aux standards sont intégrées.

4. **Build et Déploiement (optionnel)** :
   - Le pipeline peut être complété par des étapes de build et de déploiement si nécessaire.
   - Des actions GitHub peuvent être ajoutées pour automatiser le déploiement en production.

#### Variables d'environnement de test
Les variables d'environnement définies dans `ci.yml` incluent les configurations nécessaires pour PostgreSQL et les services de l'API. Ces variables peuvent être modifiées directement dans GitHub Actions pour s'adapter aux environnements de test.

## **Notes Importantes pour Toutes les APIs**

### **Fichiers `.env`**

- Les fichiers `.env` sont essentiels pour le fonctionnement des APIs.
- Ils contiennent les variables d'environnement nécessaires à la configuration des bases de données et des services externes.
- Assurez-vous que ces fichiers sont placés à la racine de chaque projet.

### **Docker Compose**

- L'utilisation de Docker Compose est recommandée pour faciliter le déploiement des services dépendants comme les bases de données et RabbitMQ.
- Les commandes `docker-compose up --build` et `docker-compose down -v` permettent de gérer facilement les conteneurs.

### **Gestion des Dépendances**

- Les fichiers `requirements.txt` listent toutes les dépendances Python nécessaires.
- Après avoir activé l'environnement virtuel, installez les dépendances avec :

  ```bash
  pip install -r requirements.txt
  ```

### **Résolution des Problèmes Courants**

- **Ports Occupés :**

  - Si un port est déjà utilisé, modifiez la variable `API_PORT` dans le fichier `.env` et ajustez les ports exposés dans le `docker-compose.yml`.

- **Problèmes de Connexion aux Bases de Données :**

  - Vérifiez que les services de base de données sont en cours d'exécution.
  - Assurez-vous que les variables d'environnement correspondent aux configurations de vos services.

- **Erreurs lors de l'Activation de l'Environnement Virtuel :**

  - Assurez-vous que vous utilisez la bonne version de Python.
  - Vérifiez les permissions du dossier `venv`.

### **Documentation et Tests**

- Chaque API est fournie avec une documentation interactive accessible via `/docs`.
- Utilisez cet outil pour tester les endpoints et comprendre les modèles de données.

### **Sécurité**

- **Variables Sensibles :**

  - Ne partagez pas vos fichiers `.env` ou toute information sensible.
  - Pour un environnement de production, utilisez des gestionnaires de secrets sécurisés.

- **Mises à Jour :**

  - Gardez vos dépendances à jour en vérifiant régulièrement le fichier `requirements.txt`.
  
### Règles d’Hébergement

1. **Sécurité des transactions** :
   - L'API Commandes gère des informations sensibles sur les commandes, nécessitant un hébergement sécurisé et l’utilisation de HTTPS.
   - Comme pour l’API Clients, veillez à sécuriser le fichier `.env` avec un gestionnaire de secrets pour éviter l’exposition des identifiants de la base de données et de RabbitMQ.

2. **Connexion à PostgreSQL** :
   - Hébergez PostgreSQL dans un environnement sécurisé et configurez-le pour n’accepter que les connexions de l’API Commandes. Utilisez des pare-feu et des VPN si possible pour ajouter une couche de sécurité.
   - Activez le chiffrement des données au repos et en transit pour PostgreSQL pour protéger les données sensibles des commandes.

3. **Disponibilité et scalabilité** :
   - Utilisez des conteneurs Docker pour l'API afin d'assurer une portabilité et une gestion efficace des ressources.
   - Privilégiez un environnement d’hébergement dans le cloud qui supporte l'autoscaling en fonction des charges (par exemple, Amazon ECS ou Azure Kubernetes).

4. **Audit et journalisation** :
   - Intégrez des outils de surveillance pour observer les performances, les erreurs et la consommation des ressources.
   - Conservez des journaux des transactions et des opérations critiques, avec des alertes configurées pour tout comportement anormal ou échec de transaction.


## Déploiement Kubernetes

Ce projet contient également les fichiers nécessaires pour déployer l'API Commandes et sa base PostgreSQL dans un cluster Kubernetes.

Les ressources créées sont :

- **Deployment** pour l'API Commandes (`api-orders`)
- **Service** de type `NodePort` pour exposer l'API (`api-orders`)
- **StatefulSet** pour la base PostgreSQL (`postgres-orders`) avec stockage persistant
- **Service** de type `Headless` (`postgres-orders`) pour PostgreSQL

### Commandes de déploiement

Appliquer les ressources Kubernetes :
```bash
kubectl apply -f api-commandes.yaml
kubectl apply -f postgres-orders.yaml
