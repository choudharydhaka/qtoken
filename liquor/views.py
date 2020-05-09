from django.shortcuts import get_object_or_404,get_list_or_404, render
from django.template import loader
from django.shortcuts import render,redirect
from django.http import Http404
from django.contrib import messages 
# Create your views here.
from django.http import HttpResponse
from .models import *
#from .forms import *
from .forms import LiquorStoreForm, StoreOwnerForm, ConsumerForm
from django.core.exceptions import MultipleObjectsReturned

#  formStore = LiquorStoreForm(request.POST)
# formOwner = StoreOwnerForm(request.POST)
# ConsumerForm(request.POST)

import datetime, string, random
import uuid;

# class LiquorStore(models.Model):
#     owner = models.ForeignKey(StoreOwnmer, on_delete=models.CASCADE)
#     name = models.CharField(max_length=200)
#     address = models.CharField(max_length=1000)
#     is_active = models.BooleanField()
#     created_date = models.DateTimeField('date Created')

def stores(request):
    if request.method == 'POST':
        owner=createNewOwner(request)
        store=createNewStore(request,owner)
        print(store.get('store_id')); 
        if store.get('store_id') is not None:
            context={
                "store_id":store.get('store_id')
            }
            return  redirect('stores/'+ store.get('store_id')+"?isNew=true")
        else:
            print(store)
            

    context={
        'StoreOwner' : StoreOwnerForm(),
        'LiquorStore': LiquorStoreForm()
    }
    return render(request, 'liquor/stores.html',context)


def index(request):

    if request.method == 'POST':
        form = ConsumerForm(request.POST)
        if form.is_valid():
            print('It a valid form')
            token=saveConsumerAndGenerateToken(request)    
            context = {
                'details': token
            }
            return render(request, 'liquor/consumer-thanks.html', context)
        else:
            print("form validation failed")
            messages.error(request, "Error")

            return render(request, 'liquor/index.html', {'form':form})

    

    return render(request, 'liquor/index.html', {'form': ConsumerForm()})


def tokens(request,store_id):
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
        for tk in Token.objects.all() :
            print(tk.store.store_id)
            if tk.store.store_id == store_id:
                print("Store found")
                tokens.append(tk)

        
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
    
    formConsumer = ConsumerForm(request.POST)
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
                created_date=datetime.datetime.now()
                #store=store
            )

            print (consumer)
            consumer.save()

        else: 
            print ("user already exist!")
        token=generateToken(consumer,store)
        return token

def getStore(request):

    form =ConsumerForm(request.POST)
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
        

def generateToken(consumer,store):
    if store is None or consumer is None: 
        print("Either consumer or store is not provided")
        return None
    token_number=token_generator()
    token=Token(
        store=store,
        consumer=consumer,
        token_valid=True,
        token_number=token_number
    )
    token.save()
    if token is None: return None
    return {'token':token_number,'address': token.store.name + " - " +token.store.address +",-" +token.store.store_id}
    
    
def token_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

def createNewOwner(request):
    formOwner = StoreOwnerForm(request.POST)
    if formOwner.is_valid():
        data=formOwner.cleaned_data
        owner=None
        try:
            print(data)
    #             mobile_number = models.CharField(max_length=10,blank=False)
    # name = models.CharField(max_length=200)
    # address = models.CharField(max_length=200)
    # pincode= models.CharField(max_length=6)
    # created_date = models.DateTimeField('date Created')
            ##{'mobile_number': '09650382883', 'name': 'suresh dhaka', 'address': 'noida', 'pincode': '301201'
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
                created_date= datetime.datetime.now()
            )
            ownerModel.save()
            print("New Store Owner has created: " + ownerModel.name)
            return ownerModel
        else:
            print("Owner already  exists : "+ owner.name)
            return owner
    


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
                created_date=datetime.datetime.now(),
                owner=owner,
                store_id=storeId
            )
            store.save()
            print("New Store has created: " + store.store_id)
        else:
            print("Store does exists already: " +  store.store_id)

        return {"store_id":store.store_id}
    












def detail(request):
    currently_registered=Consumer.objects.order_by('-created_date')
    #template = loader.get_template('liquor/index.html')
    context = {
        'consumer': currently_registered,
    }
    return render(request, 'liquor/index.html', context)
    #return HttpResponse(template.render(context, request))
    #output = ', '.join([q.name + "," + q.mobile_number + "," + q.address + "," + q.created_date.strftime("%c") for q in currently_registered])
    #return HttpResponse(output)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)