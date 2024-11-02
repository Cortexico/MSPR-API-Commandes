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
  
