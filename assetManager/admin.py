from django.contrib import admin
from .models import User, AccountType
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','email', 'first_name', 'last_name']

@admin.register(AccountType)
class UserAdmin(admin.ModelAdmin):
    list_display = ['account_type_id','user', 'account_asset_type', 'access_token','account_institution_name']
