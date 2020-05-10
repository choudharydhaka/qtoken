from django.shortcuts import get_object_or_404,get_list_or_404, render
from django.template import loader
from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib import messages 
# Create your views here.
from django.http import HttpResponse
from .models import *
#from .forms import *
from .forms import LiquorStoreForm, StoreOwnerForm, ConsumerForm,SearchStore,ConsumerFormT
from django.core.exceptions import MultipleObjectsReturned
from django.utils import timezone
import pytz

from .utils import Utils
#  formStore = LiquorStoreForm(request.POST)
# formOwner = StoreOwnerForm(request.POST)
# ConsumerForm(request.POST)

import datetime, string, random
import uuid;


SLOTS_THRESHOLD=50
# class LiquorStore(models.Model):
#     owner = models.ForeignKey(StoreOwnmer, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     address = models.CharField(max_length=1000)
#     is_active = models.BooleanField()
#     created_date = models.DateTimeField('date Created')

def stores(request):
    if request.method == 'POST':
        owner=createNewOwner(request)
        context={
            'StoreOwner' : StoreOwnerForm(request.POST),
            'LiquorStore': LiquorStoreForm(request.POST)
         }
        print(owner)
        #if owner.get("error") is not None:
            #context.update({"error":owner.get("error")})
        #else:          
        store=createNewStore(request,owner)
        if store.get("error"):
            context.update({"error":store.get("error")})
        else:
            print(store.get('store_id')); 
            if store.get('store_id') is not None:
                context={
                    "store_id":store.get('store_id')
                }
                return  redirect('stores/'+ store.get('store_id')+"?isNew=true")
            else:
                print(store)
        return render(request, 'liquor/stores.html',context)

    context={
        'StoreOwner' : StoreOwnerForm(),
        'LiquorStore': LiquorStoreForm()
    }
    return render(request, 'liquor/stores.html',context)


def searchStore(request):
    if request.method == 'POST':
        form = SearchStore(request.POST)
        stores=[]
        if form.is_valid():
            print('It a valid search form')
            print (form)
            store = None
            if form.cleaned_data.get('pincode') is not None:
                print("Store search by pincode")
                stores=LiquorStore.objects.filter(pincode= form.cleaned_data.get('pincode'))
            elif   form.cleaned_data.get('address') is not None:
                print("Store search by address")
                stores= LiquorStore.objects.filter(address= form.cleaned_data.get('address'))

            if len(stores) == 0:
                print("no store found")
                context = {
                'isSearch': True,
                'error': 'No store found!',
                'form': form
                }
                return render(request, 'liquor/index.html', context)
            else :
                print("Store has found, now rendering the list ")
                print( stores)
                context = {
                'isSearch': False,
                'stores': stores
                }  
                store_address=[ (q.store_id , q.name + " - " +q.address )  for q in stores]

                
                # SLOTS_THRESHOLD=5
                # count=0
                # store_slots=[]
                # for t in Token.objects.all():
                #     for s in stores:
                #         if t.store.store_id == s.store_id and slotTime == t.token_slot:
                #             count=count+1
                #             print(count)


                form=ConsumerForm(initial={'pickup_time':timezone.now(),'pickup_date':timezone.now().date()})
                form.setAddresses(store_address)

                #Utils().getNextSlot(start_time='9:00',end_time='18:00',slot_time=10)
                SHOP_START_TIME="09"
                SHOP_CLOSE_TIME="18"
                startTime='{:%H}'.format(datetime.datetime.now())
                #print (startTime)

                if int(startTime) <  int(SHOP_START_TIME) and int(startTime) >  int(SHOP_CLOSE_TIME):
                    startTime=SHOP_START_TIME+":00"
                else:
                    startTime=startTime+":00"
               # elif int(startTime) >  int(SHOPT_CLOSE_TIME):
                     #return render(request, 'liquor/index.html', { 'error':"Out side of working hours!",'isSearch': False,'form':form})
                
                
                slots=Utils.getNextSlot(start_time=startTime,end_time='18:00',slot_time=60)

                t_slots=[(i,i) for i in slots[0]]
                form.setPickupTime(t_slots)


                return render(request, 'liquor/index.html', { 'isSearch': False,'form':form})                   
            

        else:
            print("form validation failed for search")
            messages.error(request, "Error")
            return render(request, 'liquor/index.html', { 'isSearch': False,'form':form})    
            #redirect('liquor/index.html', { 'isSearch': False,'form':form})

    return render(request, 'liquor/index.html', { 'isSearch': True,'form': SearchStore()})#ConsumerForm(initial={'pickup_time':timezone.now()})})



def index(request):
    
    
    print("request at index")
    if request.method == 'POST':
        form = ConsumerFormT(request.POST)
        sa=request.POST.get('store_address')
        tt=request.POST.get('pickup_time')
        

        print(form)
        if form.is_valid():
            print('It a valid form')
            token=saveConsumerAndGenerateToken(request) 
            print(token)
            mobileNumber=token.get("mobile_number")
            tokenNumber=token.get("token")

            if tokenNumber is None or token.get('error'):
                return  render(request, 'liquor/index.html', {"error": token.get('error'), 'isSearch': True,'form': SearchStore()})       
            elif mobileNumber:
                twilioResp=Utils.sms(tokenNumber,mobileNumber)
                if type(twilioResp) == dict and twilioResp.get('error') is not None:
                    context = {
                'isSearch': False,
                'details': token,
                'error': "There was an error while sending the token number on your mobile, please contact support team or regenerate it."
            }
                else: 
                    context = {
                    'isSearch': False,
                    'details': token
                }
            return render(request, 'liquor/consumer-thanks.html', context)
        else:
            print("form validation failed")
            messages.error(request, "Error")

            return render(request, 'liquor/index.html', { 'isSearch': False,'form':form})

    
    return searchStore(request)
    #return render(request, 'liquor/index.html', {'isSearch': False,'form': SearchStore()})#ConsumerForm(initial={'pickup_time':timezone.now()})})


def tokens(request,store_id,day):
    print("Looking for the store: " +store_id)
    liquorStore=get_object_or_404(LiquorStore,store_id=store_id)

    context={}
    if liquorStore:
    # for a in liquorStore:
    #     print(a)
        print(liquorStore)
        print("fetching the tokens")
        tokens=[]
        #tokens=get_list_or_404(Token)
        #print(tokens)
        if str(day) == "all":
           print("All tokens")
           tokens=Token.getAllToken(store_id=store_id)            
        elif str(day)  == "today":
            print("Todays tokens")
            tokens=Token.getTodayOnly(store_id=store_id)
        else:
            print("Current tokens") 
            tokens=Token.getCurrent(store_id=store_id)
            # for tk in Token.objects.filter(pickup_date__date=datetime.datetime.now().date() ,token_slot=currentHours) :
            #     print(tk.store.store_id, datetime.datetime.now().date(), tk.pickup_date.date() )
            #     #if tk.store.store_id == store_id and  datetime.datetime.now().date() == tk.pickup_date.date() and currentHours == tk.token_slot:
            #     if tk.store.store_id == store_id :
            #         print("Store found")
            #         tokens.append(tk)

        
        context={
            'tokens': tokens,#get_list_or_404(Token),
            'store': liquorStore,
            'isNew': request.GET.get("isNew")
        }
        print(context)
    else:
        context={'error': True,'store_id': store_id}
    return render(request, 'liquor/tokens.html',context)








def getStoresAddresses():
    return  [ (q.store_id , q.name + " - " +q.address )  for q in get_list_or_404(LiquorStore)]
 


def ValidateStoreDetails(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        formOwner = StoreOwnerForm(request.POST)
        formStore = LiquorStoreForm(request.POST)
       
        # check whether it's valid:
        if formStore.is_valid()  and formOwner.is_valid():

            return True

    else:
        return False
    return False



def saveConsumerAndGenerateToken(request):
    print("Inside saveConsumerAndGenerateToken")
    formConsumer = ConsumerFormT(request.POST)
    if formConsumer.is_valid():
        data=formConsumer.cleaned_data
        store=getStore(request)
        if store is None: return None
        try:
            consumer=get_object_or_404(Consumer,name=formConsumer.cleaned_data['name'],mobile_number=formConsumer.cleaned_data['mobile_number'],pincode=formConsumer.cleaned_data['pincode'])
        except MultipleObjectsReturned :
            print("Invalid data found in Database")
            return {"error": "Possibly this Consumer already exists, please contact to support team!"}            
        except:
            consumer=None
    
        print(consumer)
        if consumer is None:
            print ("user doesn't exist!")

            consumer=Consumer(
                name=data['name'],
                address=data['address'],
                pincode=data['pincode'],

                mobile_number=data['mobile_number'],
                created_date=timezone.now()
                #store=store
            )

            print (consumer)
            consumer.save()

        else: 
            print ("user already exist!")
        token=generateToken(formConsumer,consumer,store)
        return token
    else:
        print("form is invalid")
        return {"error": "Invalid data!"}

def getStore(request):
    print("Inside getStore")
    form =ConsumerFormT(request.POST)
    if form.is_valid():
        store= get_object_or_404(LiquorStore,store_id=form.cleaned_data['store_address'])
        if store is None:
            print("Invalid Store!")
            return None
        else :
            print("A valid store found!")
            return store
    else :
        return None
        

def generateToken(formConsumer,consumer,store):
    print("Inside generateToken")    
    if store is None or consumer is None: 
        print("Either consumer or store is not provided")
        return None
    slotTime=formConsumer.cleaned_data['pickup_time']

    count=0
    for t in Token.objects.all():
        if t.store.store_id == store.store_id and slotTime == t.token_slot:
            count=count+1
            print(count)
    if count >   SLOTS_THRESHOLD:
        return {
            "error": "This time slot is exhausted, Please search again"
        } 



    token_number=token_generator()
    token=Token(
        store=store,
        consumer=consumer,
        token_slot=formConsumer.cleaned_data['pickup_time'],
        pickup_date=formConsumer.cleaned_data['pickup_date'],
        token_valid=True,
        token_number=token_number
    )
    token.save()
    if token is None: return None
    return {'mobile_number': consumer.mobile_number,
        'token':token_number,'address': token.store.name + " - " +token.store.address 
        +"," +token.store.pincode
     #+",-" +token.store.store_id
     }
    
    
def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def createNewOwner(request):
    formOwner = StoreOwnerForm(request.POST)
    if formOwner.is_valid():
        data=formOwner.cleaned_data
        owner=None
        try:
            print(data)
            owner=get_object_or_404(StoreOwner,
                    name=data['name'],
                    pincode=data['pincode'],
                    mobile_number=data['mobile_number'])
        except MultipleObjectsReturned :
            print("Invalid data found in Database")
            return {"error": "Possibly this Owner already exists, please contact to support team!"}                    
        except:
            print("No existing owner found with same details!")
            owner=None
        if owner is None:
            ownerModel=StoreOwner(
                name=data['name'],
                address=data['address'],
                pincode=data['pincode'],
                mobile_number=data['mobile_number'],
                created_date= timezone.now()
            )
            ownerModel.save()
            print("New Store Owner has created: " + ownerModel.name)
            return ownerModel
        else:
            print("Owner already  exists : "+ owner.name)
            return owner
            #return {"error": "Owner already  exists : "+ owner.name + ", Please contact to support team, you can't register same store two times."}
    


def createNewStore(request,owner):
    formStore = LiquorStoreForm(request.POST)
    storeId=token_generator()
    if formStore.is_valid():
        data=formStore.cleaned_data

        store=None
        try:

            store=get_object_or_404(LiquorStore,
                    name=data['name'],
                    pincode=data['pincode']
                    )
        except MultipleObjectsReturned :
            print("Invalid data found in Database")
            return {"error": "Possibly this Store already exists, please contact to support team!"}
        except:
            print("No existing store found with same details!")
            store=None

        if store is None:
            store=LiquorStore(
                name=data['name'],
                address=data['address'],
                pincode=data['pincode'],
                is_active=True,
                created_date=timezone.now(),
                owner=owner,
                store_id=storeId
            )
            store.save()
            print("New Store has created: " + store.store_id)
        else:
            print("Store does exists already: " +  store.store_id)
            return {"error": "Store already  exists : "+ owner.name + ", Please contact to support team, you can't register same store two times."}

        return {"store_id":store.store_id}
    









