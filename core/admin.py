from django.contrib import admin
from .models import *

admin.site.register(Role)
admin.site.register(UserProfile)
admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Invoice)
admin.site.register(Item)