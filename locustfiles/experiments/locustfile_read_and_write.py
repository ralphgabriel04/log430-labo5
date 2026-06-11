"""
Locustfile for load testing store_manager.py
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import random
from locust import HttpUser, task, between

class FlaskAPIUser(HttpUser):
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
    
    # Proportion 1:2:2, meaning: 1/5, 2/5, 2/5, because 1 + 2 + 2 = 5
    # This means 20% calls to /orders, 40% calls to /highest-spenders, 40% calls to /best-sellers
    @task(1) 
    def orders(self):
        """Test POST /orders endpoint (write)"""
        mock_order = {
            "user_id": random.randint(1, 3),
            "items": [{"product_id": random.randint(1, 4), "quantity": random.randint(1, 10)}] 
        }   

        # Randomly add a second item (30% of times)
        if random.randint(1, 10) <= 3:
            mock_order["items"].append({"product_id": random.randint(1, 4), "quantity": random.randint(1, 10)})

        with self.client.post("/orders", 
                            json=mock_order, 
                            headers={"Content-Type": "application/json"},
                            catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 201:
                    if "order_id" in data:
                        response.success()
                    else:
                        response.failure("Aucun ID renvoyé pour la commande créée")
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}")

    @task(2) 
    def highest_spenders(self):
        """Test GET /orders/reports/highest-spenders endpoint (read)"""
        with self.client.get("/orders/reports/highest-spenders", catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 200: 
                    if str(type(data)) == "<class 'list'>":
                        response.success()
                    else:
                        response.failure("Le resultat n'est pas une liste : " + str(data))
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}")

    @task(2) 
    def best_sellers(self):
        """Test GET /orders/reports/best-sellers endpoint (read)"""
        with self.client.get("/orders/reports/best-sellers", catch_response=True) as response:
            try:
                data = response.json()
                if response.status_code == 200: 
                    if str(type(data)) == "<class 'list'>":
                        response.success()
                    else:
                        response.failure("Le resultat n'est pas une liste : " + str(data))
                else:
                    response.failure(f"Erreur : {response.status_code} - {data.get('error', 'Unknown error')}")
            except ValueError:
                response.failure(f"Invalid JSON response: {response.text}")