from django.db import models
import datetime;
import uuid;    
# Create your models here
from django.utils import timezone
import pytz
import datetime

    

class Consumer(models.Model):
    mobile_number = models.CharField(max_length=200)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    pincode= models.CharField(max_length=6)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=timezone.now())

    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = timezone.now()
#    def getStore(name,mobile_number,pincode):
        

 

class StoreOwner(models.Model):
    id= models.AutoField(primary_key=True)
    mobile_number = models.CharField(max_length=10,blank=False)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    pincode= models.CharField(max_length=6)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=timezone.now())

    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = timezone.now()
    
 
class LiquorStore(models.Model):
    id= models.AutoField(primary_key=True)
    store_id= models.CharField(max_length=200,default=uuid.uuid4())
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=1000)
    pincode= models.CharField(max_length=6)    
    is_active = models.BooleanField(default=False)
    created_date = models.DateTimeField('date Created')
    updated_date = models.DateTimeField('date Updated',default=timezone.now())
    owner = models.ForeignKey(StoreOwner, on_delete=models.CASCADE)
    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['updated_date'] = timezone.now()
    #     self.fields['store_id'] = uuid.uuid4()

    
class Token(models.Model):
    id= models.AutoField(primary_key=True)
    consumer = models.ForeignKey(Consumer, on_delete=models.CASCADE)
    store = models.ForeignKey(LiquorStore, on_delete=models.CASCADE)
    token_number = models.CharField(max_length=1000)
    token_valid= models.BooleanField(default=False)
    token_slot= models.CharField(max_length=1000)
    pickup_date= models.DateTimeField('Pickup Date')
    token_created = models.DateTimeField('Token created',default=timezone.now())




# start_time = '9:00'
# end_time = '18:00'
# slot_time = 10



    def getAllToken(store_id):
        print("Get All token for the store : "+store_id)
        tokens=[]
        for tk in Token.objects.all().order_by("pickup_date","token_slot") :
            print(tk.store.store_id)
            if tk.store.store_id == store_id:
                print("Store found")
                tokens.append(tk)
        return tokens


    def getCurrent(store_id):
        print("Get All token for current time slot for the store : "+store_id)
        tokens=[]
        currentHours='{:%H}:00'.format(datetime.datetime.now())
        print( datetime.datetime.now().date())
        for tk in Token.objects.filter(pickup_date__date=datetime.datetime.now().date() ,token_slot=currentHours).order_by("token_slot") :
            print(tk.store.store_id, datetime.datetime.now().date(), tk.pickup_date.date() )
            #if tk.store.store_id == store_id and  datetime.datetime.now().date() == tk.pickup_date.date() and currentHours == tk.token_slot:
            if tk.store.store_id == store_id :
                print("Store found")
                tokens.append(tk)
        return tokens

        

    def getTodayOnly(store_id):
        print("Get All token for today only for the store : "+store_id)        
    # Get store 
    # Start date from today to next 5 day
        start_date = datetime.datetime.now().date()
        end_date = datetime.datetime.now().date() + datetime.timedelta(days=1)
        tokens=[]
        for tk in Token.objects.filter(pickup_date__date=start_date).order_by("token_slot")  :
            print(tk.store.store_id)
            if tk.store.store_id == store_id:
                print("Store found")
                tokens.append(tk)

  
        
  
        return tokens       
    # def __init__(self, *args, **kwargs):
    #     super(Consumer, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     self.fields['token_date'] = timezone.now()