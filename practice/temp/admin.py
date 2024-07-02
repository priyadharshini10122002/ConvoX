from django.contrib import admin
from .models import Rooom, Topic, Messages, User

# Register your models here.
admin.site.register(User)
admin.site.register(Rooom)

admin.site.register(Topic)

admin.site.register(Messages)


