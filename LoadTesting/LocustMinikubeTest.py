import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.get("/run?price=20.00&fixedCost=100.00&unitCost=10.00")
        

    def on_start(self):
       self.client.get("/run?price=20.00&fixedCost=100.00&unitCost=10.00")