import random
import json
from locust import HttpUser, task, between

class QuickstartUser(HttpUser):
    wait_time = between(5, 9)

 #   @task
 #   def index_page(self):
 #       self.client.get("/function/break-even-kotlin")
        
    @task    
    def create_post(self):
        headers = {'content-type': 'application/json','Accept-Encoding':'gzip'}
        self.client.post("/function/break-even-kotlin",data= json.dumps({
      "price": 10.0,
      "fixedCosts": 100.0,
      "unitCosts": 20.0
    }), 
    headers=headers, 
    name = "break-even-kotlin")
