from django.db import models


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name
    
class STKPayment(BaseModel):
<<<<<<< HEAD
    MerchantRequestID = models.TextField(max_length=100)
    CheckoutRequestID = models.TextField(max_length=100)
    ResultDesc = models.TextField(max_length=100)      
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.TextField(max_length=100)
    TransactionDate = models.DateTimeField(max_length=100)    
    phone_number = models.TextField(max_length=20)    
=======
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_code = models.TextField()
    phone_number = models.TextField()    
>>>>>>> 17c0a8f0b85077de1abffd6861f1c3a8295c6a91
    

    class Meta:
        verbose_name = 'STK Payment'
        verbose_name_plural = 'stk Payments'

    def __str__(self):
<<<<<<< HEAD
        return self.phone_number
=======
        return self.amount
>>>>>>> 17c0a8f0b85077de1abffd6861f1c3a8295c6a91
