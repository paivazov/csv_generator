from django.contrib import admin

from planeks_csv_generator.csv_generator.models import DataSet, DataColumn


class DataColumnInLineAdmin(admin.TabularInline):
    model = DataColumn


class DataSetAdmin(admin.ModelAdmin):
    inlines = [DataColumnInLineAdmin]


admin.site.register(DataSet, DataSetAdmin)
