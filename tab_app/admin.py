from django.contrib import admin
from .models import TabRecord
from .models import Employee, Tabel

@admin.register(TabRecord)
class TabRecordAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'date', 'revenue', 'expenses', 'profit')
    list_filter = ('company_name', 'date')
    search_fields = ('company_name',)

admin.site.site_header = "Управление табельным учетом"
admin.site.index_title = "Администрирование данных"
admin.site.register(Employee)
admin.site.register(Tabel)
