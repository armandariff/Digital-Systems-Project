from django.contrib import admin

from import_export.resources import ModelResource
from import_export.admin import ImportExportModelAdmin

from .models import Movie, Genre, WatchList

# Register your models here.

class MovieResource(ModelResource):
    
    def before_save_instance(self, instance, using_transactions, dry_run):
        if not instance.runtime:
            instance.runtime = 0
        return super().before_save_instance(instance, using_transactions, dry_run)
    
    def before_import_row(self, row, row_number=None, **kwargs):
        return super().before_import_row(row, row_number, **kwargs)
    
    class Meta:
        model = Movie

class MovieAdmin(ImportExportModelAdmin):
    resource_classes = [MovieResource]
        
admin.site.register(Movie, MovieAdmin)
admin.site.register(Genre)
admin.site.register(WatchList)
