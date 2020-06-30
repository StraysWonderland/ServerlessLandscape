import random
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

    @task
    def index_page(self):
        self.client.post("/function/markdown", {"# locust load test *client posting to markdown function"})
        

    def on_start(self):
       self.client.get("/function/nodeinfo")