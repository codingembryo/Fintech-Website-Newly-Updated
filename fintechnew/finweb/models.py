from django.db import models

class Category(models.Model):
    identifier = models.CharField(max_length=100, default="data")
    name = models.CharField(max_length=200)

# define a string representation of the model
    def __str__(self):
        return self.name

#airtime & data service    
class NetworkService(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    service_name=models.CharField(max_length=50) #mtn, glo, airtime, 
    service_id=models.CharField(max_length=25) #mtn-data, glo-data, airtime-data
    logo=models.ImageField(upload_to="service_logo")

    def __str__(self):
        return f"{self.service_name}-service"

