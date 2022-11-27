from django.contrib import admin

from chatterapp.models import *

# Register your models here.
admin.site.register(Theme)
admin.site.register(Room)
admin.site.register(Message)
admin.site.register(MyUser)

