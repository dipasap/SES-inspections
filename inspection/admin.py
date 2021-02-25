from django.contrib import admin
from .models import *
# Register your models here.


class DeviceInline(admin.StackedInline):
    model = Device
    extra = 1

class QuestionCategoryInline(admin.StackedInline):
    model = QuestionCategory
    extra = 1

    def get_formset(self, request, inspection_entity_obj, *args, **kwargs):
        formset = super(QuestionCategoryInline, self).get_formset(request, inspection_entity_obj, *args, **kwargs)
        if inspection_entity_obj:
            formset.form.base_fields["entity"].queryset = inspection_entity_obj.question_categories.all()
            formset.form.base_fields["device"].queryset = inspection_entity_obj.device.all()
        return formset

class QuestionInline(admin.StackedInline):
    model = Question
    extra = 1

    def get_formset(self, request, inspection_entity_obj, *args, **kwargs):
        formset = super(QuestionInline, self).get_formset(request, inspection_entity_obj, *args, **kwargs)
        if inspection_entity_obj:
            formset.form.base_fields["entity"].queryset = inspection_entity_obj.question_categories.all()
            formset.form.base_fields["device"].queryset = inspection_entity_obj.device.all()
            formset.form.base_fields["category"].queryset = inspection_entity_obj.question_categories.all()
        return formset

class QuestionEntityAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_by']
    inlines = [DeviceInline, QuestionCategoryInline, QuestionInline]
        



admin.site.register(Device)
admin.site.register(InspectionType)
admin.site.register(Inspection)
admin.site.register(InspectionReport)
admin.site.register(InspectionEntity, QuestionEntityAdmin)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Answer)
admin.site.register(QuestionCategory)
admin.site.register(DeviceInspection)
