# Django imports
from django.contrib import admin

# Project imports
from project.inauth.models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ('email', 'created_at')


class PasswordResetRequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'used', 'created_at')


class ConfirmationAccountRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'confirmed', 'send_count', 'created_at')


admin.site.register(User, UserAdmin)
admin.site.register(PasswordResetRequest, PasswordResetRequestAdmin)
admin.site.register(ConfirmationAccountRequest, ConfirmationAccountRequestAdmin)