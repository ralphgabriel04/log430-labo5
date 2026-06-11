# Labo 05 – Microservices, SOA, SBA, API Gateway, Rate Limit & Timeout

<img src="https://upload.wikimedia.org/wikipedia/commons/2/2a/Ets_quebec_logo.png" width="250">    
ÉTS - LOG430 - Architecture logicielle - Chargé de laboratoire: Gabriel C. Ullmann.

## 🎯 Objectifs d'apprentissage
- Apprendre à communiquer avec un microservice déjà existant
- Apprendre à configurer et utiliser KrakenD, un API Gateway
- Découvrir les configurations de `timeout` (limitation du temps de réponse) et `rate limiting` (limitation du nombre de requêtes) dans KrakenD

## ⚙️ Setup

Dans ce labo, nous allons ajouter des fonctionnalités de paiement à notre application Store Manager. Ainsi comme nous avons les répertoires `orders` et `stocks` dans notre projet, nous pourrions simplement ajouter un répertoire `payments` et commencer à écrire nos fonctionnalités de paiement. Cependant, il vaut mieux développer une application complètement isolée dans un dépôt séparé - un microservice - pour les paiements au lieu de l'ajouter au Store Manager. Ça nous donne plus de flexibilité de déploiement et d'évolution. Pour en savoir plus, veuillez lire la documentation architecturale dans le répertoire `/docs/arc42/architecture.pdf`.

> ⚠️ ATTENTION : Pendant ce laboratoire, nous allons travailler avec ce dépôt (`log430-labo5`), ainsi qu'avec un **deuxième dépôt**, [log430-labo5-paiement](https://github.com/guteacher/log430-labo5-payment). Veuillez lire le document `/docs/adr/adr001.md` dans `log430-labo5-paiement` pour comprendre notre choix de créer un microservice séparé pour les fonctionnalités de paiement.

### 1. Clonez les dépôts
Créez vos propres dépôts à partir des dépôts gabarits (templates). Vous pouvez modifier la visibilité pour les rendre privés si vous voulez.
```bash
git clone https://github.com/[votrenom]/log430-labo5
git clone https://github.com/[votrenom]/log430-labo5-payment
cd log430-labo5
```
Ensuite, clonez votre dépôt sur votre ordinateur et sur votre serveur de déploiement (ex. VM). Veillez à ne pas cloner le dépôt d'origine.

Ensuite, veuillez faire les étapes de setup suivantes pour les **deux dépôts**.

### 2. Créez un fichier .env
Créez un fichier `.env` basé sur `.env.example`. Dans le fichier `.env`, utilisez les mêmes identifiants que ceux mentionnés dans `docker-compose.yml`. Veuillez suivre la même approche que pour les derniers laboratoires.

### 3. Créez un réseau Docker
Exécutez dans votre terminal :
```bash
docker network create labo05-network
```

### 4. Préparez l'environnement de développement
Suivez les mêmes étapes que pour les derniers laboratoires.
```bash
docker compose build
docker compose up -d
```

### 5. Préparez l'environnement de déploiement et le pipeline CI/CD
Utilisez les mêmes approches qui ont été abordées lors des derniers laboratoires.

## 🧪 Activités pratiques

### 1. Intégration du service de paiement
Dans `orders/commands/write_order.py`, la fonction `add_order` effectue la création des nouvelles commandes. Dans cette version de l'application, elle va également accomplir une étape supplémentaire : demander à un service de paiement la création d'une transaction de paiement, que nous garderons sous forme de lien avec la commande pour que, plus tard, on puisse payer pour la commande.

**Votre tâche :** dans `orders/commands/write_order.py`, complétez l'implémentation de la fonction `request_payment_link` pour faire un appel POST à l'endpoint `/payments` dans le service de paiement et obtenir le `payment_id`.

```python
  response_from_payment_service = requests.post('url-to-api-gateway',
      json=payment_transaction,
      headers={'Content-Type': 'application/json'}
  )
```

> ⚠️ ATTENTION : Pour connaître l'URL du service de paiement, veuillez regarder dans `config/krakend.json`. Nous n'allons pas appeler le service directement, nous appellerons KrakenD et il s'occupera d'acheminer notre requête vers le bon chemin. Même si les endpoints du service de paiement ou les hostnames changent, si nous maintenons KrakenD à jour, aucune modification n'est nécessaire dans l'application Store Manager.

> 💡 **Question 1** : Quelle réponse obtenons-nous à la requête à `POST /payments` ? Illustrez votre réponse avec des captures d'écran/du terminal.

### 2. Utilisez le lien de paiement
- Dans votre Postman, importez la collection Postman qui est dans `docs/collections` à `log430-labo5`
- Ensuite, importez aussi la collection sur `docs/collections` à `log430-labo5-payment`

#### Dans `log430-labo5`
- Créez une commande avec `POST /orders`. Vous obtiendrez un `order_id`.
- Cherchez la commande avec `GET /order/:id`. Vous obtiendrez un `payment_id`.

#### Dans `log430-labo5-payment`
- Faites une requête à `POST payments/process/:id` en utilisant le `payment_id` obtenu. Regardez l'onglet "Body" pour voir ce qu'on est en train d'envoyer dans la requête.
- Faites une requête à `GET payments/:id` en utilisant le `payment_id` obtenu. Observez le résultat pour savoir si le paiement a été réalisé correctement.

> 💡 **Question 2** : Quel type d'information envoyons-nous dans la requête à `POST payments/process/:id` ? Est-ce que ce serait le même format si on communiquait avec un service SOA, par exemple ? Illustrez votre réponse avec des exemples et captures d'écran/terminal.

> 💡 **Question 3** : Quel résultat obtenons-nous de la requête à `POST payments/process/:id`?

### 3. Ajoutez un nouveau endpoint à KrakenD
Ajoutez l'endpoint de création de commandes à `config/krakend.json`. Nous l'utiliserons lors des prochaines activités. Ce code ajoute une [limitation du nombre de requêtes](https://www.krakend.io/docs/endpoints/rate-limit/) à nos endpoints (par minute, par client).
```json
  {
      "endpoint": "/store-manager-api/orders",
      "method": "POST",
      "backend": [
        {
          "url_pattern": "/orders",
          "host": ["http://store_manager:5000"],
        }
      ],
      "extra_config": {
        "qos/ratelimit/router": {
          "max_rate": 200,
          "every": "1m",
        }
      }
  },
  {
    "endpoint": "/store-manager-api/orders",
    "method": "PUT",
    "backend": [
      {
        "url_pattern": "/orders",
        "host": ["http://store_manager:5000"],
      }
    ]
  },
```

Ensuite, **reconstruisez et redémarrez** le conteneur Docker. 

### 4. Mettez à jour la commande après le paiement
Si les étapes de l'activité 2 fonctionnent, cela signifie que les paiements sont traités correctement. Cependant, si ces informations restent dans le service de paiement, elles ne sont pas très utiles. Modifiez `log430-labo05-payment` pour faire en sorte qu'il appelle l'endpoint `PUT /orders` dans `log430-labo05` pour mettre à jour la commande de (modifier `is_paid` à `true`). Utilisez les documents architecturaux disponibles dans `log430-labo05-payment` pour comprendre le fonctionnement du service et déterminer quel module ou quelle méthode doit être modifié(e).

> ⚠️ ATTENTION : N'oubliez pas d'appeler l'endpoint tel que décrit dans `config/krakend.json`.

> 💡 **Question 4** : Quelle méthode avez-vous dû modifier dans `log430-labo05-payment` et qu'avez-vous modifiée ? Justifiez avec un extrait de code.

### 5. Testez le rate limiting avec Locust
En plus de fonctionner en tant qu'une façade pour nos APIs, nous pouvons aussi utiliser KrakenD pour limiter l'accès à nos APIs et les protéger des attaques DDOS, par exemple. Nous faisons ça avec rate limiting. Créez un nouveau test dans `locustfiles/locustfile.py` spécifiquement pour tester le rate limiting :

```python
  @task(1)
  def test_rate_limit(self):
      """Test pour vérifier le rate limiting"""
      payload = {
          "user_id": random.randint(1, 3),
          "items": [{"product_id": random.randint(1, 4), "quantity": random.randint(1, 10)}] 
      }   
      
      response = self.client.post(
          "/store-manager-api/orders",
          json=payload
      )
      
      if response.status_code == 503:  # HTTP 503 Service Unavailable
          print("Rate limit atteint!")
```

Changez la ligne ci-dessous dans `docker-compose.yml` :

Avant:
```yml
command: -f /mnt/locust/locustfile.py --host=http://store_manager:5000

```

Après:
```yml
command: -f /mnt/locust/locustfile.py --host=http://api-gateway:8080
```

**Reconstruisez et redémarrez** le conteneur Docker. Ensuite, dans votre navigateur, accédez à `http://localhost:8089` et configurez Locust avec :
- Number of users : 100 (total)
- Spawn rate : 1 (par seconde)
- Host : `http://api-gateway:8080` (l'adresse à KrakenD)

Lancez le test et observez les réponses HTTP 503 (Service Unavailable).

> 💡 **Question 5** : À partir de combien de requêtes par minute observez-vous les erreurs 503 ? Justifiez avec des captures d'écran de Locust.

### 6. Créez un endpoint de test pour le timeout
Dans `store_manager.py`, ajoutez un endpoint de test qui simule une réponse lente :

```python
import time

@app.get('/test/slow/<int:delay_seconds>')
def test_slow_endpoint(delay_seconds):
    """Endpoint pour tester les timeouts"""
    time.sleep(delay_seconds)  # Simule une opération lente
    return {"message": f"Response after {delay_seconds} seconds"}, 200
```

De plus, ajoutez cet endpoint à `config/krakend.json`. Ensuite, **reconstruisez et redémarrez** le conteneur Docker. 
```json
  {
    "endpoint": "/store-manager-api/test/slow/{delay}",
    "method": "GET",
    "backend": [
      {
        "url_pattern": "/test/slow/{delay}",
        "host": ["http://store_manager:5000"],
        "timeout": "5s"
      }
    ]
  }
```

Testez différents délais en utilisant votre navigateur :
- `http://localhost:8080/store-manager-api/test/slow/2` 
- `http://localhost:8080/store-manager-api/test/slow/10` 

> 💡 **Question 6** : Que se passe-t-il dans le navigateur quand vous faites une requête avec un délai supérieur au timeout configuré (5 secondes) ? Quelle est l'importance du timeout dans une architecture de microservices ? Justifiez votre réponse avec des exemples pratiques.

### 7. Éxécutez un test de charge
Exécutez un test de charge sur l'application Store Manager en utilisant Locust. 
- Si possible, déployez Store Manager et le service de paiement dans deux VMs distinctes.
- Le cas échéant, modifiez le `host` cible sur Locust pour qu'il corresponde à l'adresse IP de la VM qui héberge l'application Store Manager.
- Suivez les mêmes instructions que celles du laboratoire 4, activité 5. 
- Testez la création d'une commande et notez vos observations sur les performances dans le rapport.

### 8. Déploiement avec Kubernetes (facultatif)
L'adoption d'une architecture en microsservices soulève un défi important : le déploiement se complexifie, surtout lorsque chaque service est hébergé sur un serveur distinct. Bien qu'il soit possible d'automatiser les tests et le déploiement via GitHub CI, la configuration doit être répétée pour chaque nouvelle VM ou serveur, et il faut s'assurer que tous exécutent la dernière version du code.

Pour simplifier et mieux mettre à l'échelle ce processus, il est recommandé d'utiliser un orchestrateur de conteneurs tel que [Kubernetes](https://github.com/kubernetes/kubernetes) (k8s). Consultez le tutoriel dans le fichier `ks3.md` pour en savoir plus. Bien que vos compétences en Kubernetes ne soient pas évaluées dans ce laboratoire, elles peuvent s'avérer précieuses lors du déploiement de votre projet.

## 📦 Livrables

- Un fichier .zip contenant l'intégralité du code source du projet Labo 05.
- Un rapport en .pdf répondant aux questions présentées dans ce document. Il est obligatoire d'illustrer vos réponses avec du code ou des captures d'écran/terminal.
