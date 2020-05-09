from django import forms
from django.shortcuts import get_object_or_404,get_list_or_404
from .models import LiquorStore

def getStoresAddresses():
    return  [ (q.store_id , q.name + " - " +q.address )  for q in LiquorStore.objects.all()] or []
#def getStoresAddresses(): return [('123','123')]

class ConsumerForm(forms.Form):
    mobile_number = forms.CharField(label='Consumer Mobile Number', max_length=200,required=True)
    name = forms.CharField(label='Consumer Name',max_length=200,required=True)
    address = forms.CharField(label='Consumer Address', max_length=1000,required=True)
    pincode = forms.CharField(label='Consumer pincode', max_length=6,required=True)
    store_address = forms.ChoiceField(label='Store address',required=True,choices=tuple(getStoresAddresses()))
    



    # def __init__(self, store_addresses, *args, **kwargs):
    #     super(ConsumerForm, self).__init__(*args, **kwargs)
    #     #self.fields['store_addresses'] = forms.ChoiceField(choices=tuple([(name, name) for name in round_list]))
    #     if store_addresses is not None:
    #         self.fields['store_address'] = forms.ChoiceField(choices=tuple(store_addresses))

    # def _storeAddress(self, value):
    #     # we overwrite this function so no list(value) is called
    #     self._choices = self.widget.choices = value

class StoreOwnerForm(forms.Form):
    mobile_number = forms.CharField(label='Mobile Number', max_length=200)
    name = forms.CharField(label='Full Name', max_length=200)
    address = forms.CharField(label='Address', max_length=200)
    pincode = forms.CharField(label='pincode', max_length=200)    


class LiquorStoreForm(forms.Form):
    name = forms.CharField(label='Registered Name', max_length=200)
    address = forms.CharField(label='Address', max_length=1000)
    pincode= forms.CharField(label='Pincode', max_length=6)    

