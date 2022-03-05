from django.contrib import admin
from . import models

# Register your models here.
class SFNArticlesAdmin(admin.ModelAdmin):
    list_display = ('title', )


class SFNArticlesEventsAdmin(admin.ModelAdmin):
    pass


class SFNArticlesLaunchesAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.SFNArticles, SFNArticlesAdmin)
admin.site.register(models.SFNArticlesEvents, SFNArticlesEventsAdmin)
admin.site.register(models.SFNArticlesLaunches, SFNArticlesLaunchesAdmin)
