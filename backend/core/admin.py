from django.contrib import admin
from . import models


class MessageInline(admin.StackedInline):
    model = models.Message
    exclude = ('from_user',)
    extra = 1

    def has_change_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('state', )

    inlines = (MessageInline,)

    def has_add_permission(self, *args, **kwargs):
        return False

    def has_delete_permission(self, *args, **kwargs):
        return False
