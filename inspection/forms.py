from django import forms
from inspection.models import Inspection, InspectionType, Device, InspectionEntity, QuestionCategory, Question, InspectionReport
from django.forms.formsets import formset_factory
from django.forms.models import inlineformset_factory

class InspectionEntityForm(forms.ModelForm):

    class Meta:
        model = InspectionEntity
        fields = ["name", "description", "logo", "address", "created_by"]
        widgets = {'created_by': forms.HiddenInput()}

class InspectionTypeForm(forms.ModelForm):

    class Meta:
        model = InspectionType
        fields = ["name", "description", "created_by"]
        widgets = {'created_by': forms.HiddenInput()}

class DeviceForm(forms.ModelForm):

    class Meta:
        model = Device
        fields = ["entity", "inspection_type", "inspector", "name", "description", "assigned_by"]
        widgets = {'assigned_by': forms.HiddenInput()}

DeviceFormset = inlineformset_factory(
        InspectionEntity, 
        Device, 
        fields=(
            'name',
            'description',
            'inspection_type',
            'inspector',
            'assigned_by'
        ),
        extra=1,
    )

class QuestionCategoryForm(forms.ModelForm):

    class Meta:
        model = QuestionCategory
        fields = ["entity", "device", "title", "slug", "description", "created_by"]
        widgets = {'created_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.none()

        if 'entity' in self.data:
            try:
                entity_id = int(self.data.get('entity'))
                self.fields['device'].queryset = Device.objects.filter(entity_id=entity_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['device'].queryset = self.instance.entity.device

QuestionCategoryFormset = inlineformset_factory(
        InspectionEntity,
        QuestionCategory,
        QuestionCategoryForm,
        extra=1
    )

class QuestionForm(forms.ModelForm):

    class Meta:
        model = Question
        fields = ["entity", "device", "category", "question_text", "answer_type", "choices", "created_by"]
        widgets = {'created_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['device'].queryset = Device.objects.none()
        self.fields['category'].queryset = QuestionCategory.objects.none()

        if 'entity' in self.data:
            try:
                entity_id = int(self.data.get('entity'))
                self.fields['device'].queryset = Device.objects.filter(entity_id=entity_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['device'].queryset = self.instance.entity.device

        if 'device' in self.data:
            try:
                device_id = int(self.data.get('device'))
                self.fields['category'].queryset = QuestionCategory.objects.filter(device_id=device_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['category'].queryset = self.instance.device.category

QuestionFormset = inlineformset_factory(
        QuestionCategory,
        Question,
        fields=(
            "question_text", 
            "answer_type", 
            "choices", 
            "created_by"
        ),
        extra=1
    )
class InspectionForm(forms.ModelForm):

    class Meta:
        model = Inspection
        fields = ["name", "entity", "devices", "inspectors", "inspection_type", "start_date_time", "created_by"]
        widgets = {'created_by': forms.HiddenInput()}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['devices'].queryset = Device.objects.none()

        if 'entity' in self.data:
            try:
                entity_id = int(self.data.get('entity'))
                self.fields['devices'].queryset = Device.objects.filter(entity_id=entity_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty City queryset
        elif self.instance.pk:
            self.fields['devices'].queryset = self.instance.entity.device


class InspectionReportForm(forms.ModelForm):

    class Meta:
        model = InspectionReport
        fields = ["inspection", "user", "pdf", "is_active", "reported_datetime"]
