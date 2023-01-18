from django.contrib import admin
from app_shop.models import Category, Product, Subcategory, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['category_name', 'slug']
    prepopulated_fields = {'slug': ('category_name', )}

@admin.register(Subcategory)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']



@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'available', 'created', 'uploaded']
    list_filter = ['available', 'created', 'uploaded']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name', )}


@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['author', 'created', 'descriptions',]
