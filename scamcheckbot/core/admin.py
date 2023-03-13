from django.contrib import admin

from .models import Profiles, Scammers, Scammersdata


@admin.register(Profiles)
class ProfilesAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'userid',
        'regdate',
        'usedate',
    ]


@admin.register(Scammers)
class ScammersAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'taxid',
        'added',
        'fraudcount',
        'fraudsum',
        'comment',
    ]


@admin.register(Scammersdata)
class ScammersdataAdmin(admin.ModelAdmin):
    list_display = [
        'scammer',
        'tel',
        'tg',
        'card',
    ]