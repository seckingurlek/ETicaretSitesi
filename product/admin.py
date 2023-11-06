from django.contrib import admin
from .models import Category, Product, Images

class ProductImageInLine(admin.TabularInline):
    model = Images
    extra = 5


# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'status']
    list_filter = ['status']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title','category','price','amount', 'status']
    list_filter = ['status','category']
    inlines = [ProductImageInLine]

class ImagesAdmin(admin.ModelAdmin):
    list_display = ['title','product','image']


admin.site.register(Category,CategoryAdmin)
admin.site.register(Product,ProductAdmin)
admin.site.register(Images, ImagesAdmin)

