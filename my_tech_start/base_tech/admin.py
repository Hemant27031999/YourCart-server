from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *

# Register your models here.
admin.site.register(Orders)
admin.site.register(RegUser)
@admin.register(Vendors)
class VendorsAdmin(ImportExportModelAdmin):
	pass
