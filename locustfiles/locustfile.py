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
        """Test pour vérifier le rate limiting"""
        # TODO: écrivez le test
        print("Test")