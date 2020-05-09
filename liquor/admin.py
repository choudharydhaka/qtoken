from django.contrib import admin

from .models import *

admin.site.register(Consumer)
admin.site.register(StoreOwner)
admin.site.register(LiquorStore)
admin.site.register(Token)
