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

    def on_start(self):
        """Called every time a Locust user spawns"""
        print("Welcome, user!")

    @task(1)
    def test_rate_limit(self):
        """Test pour vérifier le rate limiting de KrakenD sur POST /store-manager-api/orders"""
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
