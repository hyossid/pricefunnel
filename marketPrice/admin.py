from django.contrib import admin
from MarketPrice.models import StockPrice


class StockPriceAdmin(admin.ModelAdmin):
    pass


admin.site.register(StockPrice, StockPriceAdmin)
