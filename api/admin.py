from django.contrib import admin
from api.models import RetailObject, Contact, Address, Product, Employee
from api.tasks import reset_debt_task


class RetailObjectModelInline(admin.TabularInline):
    model = RetailObject


@admin.register(RetailObject)
class RetailObjectAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "debt", "type", "provider_link", "level")
    list_filter = ("contact__address__city",)
    search_fields = ("name", "debt", "type")
    inlines = [RetailObjectModelInline]

    @admin.action(description="reset_debt")
    def reset_debt(self, request, queryset):
        if len(queryset) <= 20:
            queryset.update(debt=0)
            return queryset
        else:
            reset_debt_task(queryset)

    actions = [reset_debt]


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("id", "email", "address")
    list_filter = ("email", "address")
    search_fields = ("email", "address")


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ("id", "country", "city", "street", "house_number")
    list_filter = ("country", "city", "street", "house_number")
    search_fields = ("country", "city", "street", "house_number")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "product_model", "release_date")
    list_filter = (
        "name",
        "product_model",
        "release_date",
    )
    search_fields = ("name", "product_model", "release_date")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ("id", "first_name", "last_name", "email", "created_at")
    list_filter = ("first_name", "email", "created_at")
    search_fields = ("first_name", "last_name", "email", "created_at")
