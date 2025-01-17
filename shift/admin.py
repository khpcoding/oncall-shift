from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from .models import Shift
import datetime
import jdatetime

class ShiftResource(resources.ModelResource):

    day_of_week = fields.Field(attribute='day_of_week', column_name='DayOfWeek')
    status = fields.Field(attribute='status', column_name='Status')
    shift_type = fields.Field(attribute='shift_type', column_name='Shift_Type')
    date = fields.Field(attribute='date', column_name='Date')
    start_time = fields.Field(attribute='start_time', column_name='StartTime')
    end_time = fields.Field(attribute='end_time', column_name='EndTime')
    name = fields.Field(attribute='name', column_name='NAME')

    def before_import(self, dataset, **kwargs):
        Shift.objects.all().delete()
        return super().before_import(dataset, **kwargs)
    
    def before_save_instance(self, instance, row, **kwargs):
        jalali_date = jdatetime.date.fromisoformat(instance.date.replace('.', '-'))
        instance.date = jalali_date.togregorian()

        if '.' in instance.start_time:
            instance.start_time = datetime.datetime.strptime(instance.start_time, '%H.%M').time()
        else:
            instance.start_time = datetime.datetime.strptime(instance.start_time, '%H').time()
        
        if '.' in instance.end_time:
            instance.end_time = datetime.datetime.strptime(instance.end_time, '%H.%M').time()
        else:
            instance.end_time = datetime.datetime.strptime(instance.end_time, '%H').time()

        return super().before_save_instance(instance, row, **kwargs)
    

    class Meta:
        model = Shift
        fields = ('day_of_week', 'status', 'shift_type', 'date', 'start_time', 'end_time', 'name')
        skip_unchanged = True
        report_skipped = True

    def get_instance(self, instance_loader, row):
        return None

class ShiftAdmin(ImportExportModelAdmin):
    resource_class = ShiftResource
    list_display = ('day_of_week', 'status', 'shift_type', 'date', 'start_time', 'end_time', 'name')

admin.site.register(Shift, ShiftAdmin)
