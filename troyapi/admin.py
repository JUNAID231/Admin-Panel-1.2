from django.contrib import admin
from .models import User, Transaction, News, Admin, Chat, ChatUser
# Register your models here.

admin.site.register(User)
admin.site.register(Transaction)
admin.site.register(News)
admin.site.register(Admin)
admin.site.register(Chat)
admin.site.register(ChatUser)