from django.contrib import admin
from main_app.models import Product, Employee


@admin.register(Product)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_on')
    search_fields = ('name', 'category', 'supplier')
    list_filter = ('category', 'supplier')
    fieldsets = (
        ("General Information", {
            'fields': ("name", "description", "price", "barcode")
        }),
        ("Categorization", {
            'fields': ("category", "supplier")
        }),
    )
    readonly_fields = ('created_on', 'last_edited_on')
    date_hierarchy = 'created_on'

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'position', 'department')