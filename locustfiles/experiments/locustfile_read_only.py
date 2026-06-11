"""
Locustfile for load testing store_manager.py
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
from locust import HttpUser, task, between

class FlaskAPIUser(HttpUser):
    # Wait time between requests (1-3 seconds)
    wait_time = between(1, 3)
    
    # Proportion 1:1, meaning 1/2 + 1/2
    # This means 50% calls to /highest-spenders, 50% calls to /best-sellers
    @task(1) 
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
                response.failure(f"Invalid JSON response: {response.text}, code {response.status_code}")

    @task(1) 
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
                response.failure(f"Invalid JSON response: {response.text}, {response.status_code}")