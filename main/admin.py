from django.contrib import admin
from .models import Settings, Image, CarouselItemModel, ColorModel, SizeModel, ImageTypeModel, ContactModel

# Register your models here.

@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    pass

@admin.register(ContactModel)
class ContactAdmin(admin.ModelAdmin):
    pass

@admin.register(ImageTypeModel)
class ImageTypeAdmin(admin.ModelAdmin):
    pass

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    pass

@admin.register(ColorModel)
class ColorAdmin(admin.ModelAdmin):
    pass

@admin.register(SizeModel)
class SizeAdmin(admin.ModelAdmin):
    pass


@admin.register(CarouselItemModel)
class CarouselItemAdmin(admin.ModelAdmin):
    pass