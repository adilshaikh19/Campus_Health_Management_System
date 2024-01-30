from django.db import models

# Create your models here.

class Medicine(models.Model):
    name = models.CharField(unique = True, max_length = 150)
    company = models.CharField(max_length = 150)
    manufacturedDate = models.DateField()
    expiryDate = models.DateField()
    quantity = models.PositiveIntegerField()
    price = models.PositiveIntegerField()
    photoId = models.CharField(unique = True, max_length = 100)

    def __str__(self):
        return "Name : " + str(self.name) + " Company : " + str(self.company) + " Manufactured Date : " + str(self.manufacturedDate) + " Expiry Date : " + str(self.expiryDate) + " Quantity : " + str(self.quantity)
    

class Purchase(models.Model):
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    buyer_name = models.CharField(max_length=100)
    buyer_email = models.EmailField()
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    purchase_date = models.DateTimeField(auto_now_add=True)
    address = models.TextField(default="N/A")
    def __str__(self):
        return f'{self.quantity} {self.medicine.name} purchased by {self.buyer_name}'
