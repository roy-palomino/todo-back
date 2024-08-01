from django.contrib import admin
from .models import Task, Category, Tag, UserSettings


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(UserSettings)
class UserSettings(admin.ModelAdmin):
    pass
