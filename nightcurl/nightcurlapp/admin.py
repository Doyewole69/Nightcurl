from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, UserAddress
from .forms import UserChangeForm, UserCreationForm

class CustomUserAdmin(UserAdmin):
    model = User
    add_form = UserCreationForm
    form = UserChangeForm
    ordering = ('email',)


admin.site.register(User, CustomUserAdmin)
admin.site.register(UserAddress)
