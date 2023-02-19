from django.contrib import admin

from.models import *
# Register your models here.
admin.site.register(posts)
admin.site.register(User)
admin.site.register(follow)
admin.site.register(likes)
