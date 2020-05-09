from django.db import models
import datetime;
import uuid;    
# Create your models here


    

class Consumer(models.Model):
    mobile_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    pincode= models.CharField(max_length=6)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=datetime.datetime.now())

    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = datetime.datetime.now()
#    def getStore(name,mobile_number,pincode):
        

 

class StoreOwner(models.Model):
    id= models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=10,blank=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pincode= models.CharField(max_length=6)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=datetime.datetime.now())

    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = datetime.datetime.now()
    
 
class LiquorStore(models.Model):
    id= models.AutoField(primary_key=True)
    store_id= models.CharField(max_length=200,default=uuid.uuid4())
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    pincode= models.CharField(max_length=6)    
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=datetime.datetime.now())
    owner = models.ForeignKey(StoreOwner, on_delete=models.CASCADE)
    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = datetime.datetime.now()
    #     self.fields['store_id'] = uuid.uuid4()

    
class Token(models.Model):
    id= models.AutoField(primary_key=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    store = models.ForeignKey(LiquorStore, on_delete=models.CASCADE)
    token_number = models.CharField(max_length=1000)
    token_valid= models.BooleanField(default=False)
    token_created = models.DateTimeField('Token created',default=datetime.datetime.now())

    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['token_date'] = datetime.datetime.now()