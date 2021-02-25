from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.urls import reverse

# Create your models here.

INSPECTION_ENTITY_TYPE = (
    ('hospital', 'Hospital'),
    ('governace_house', 'Governance House')
)
TEXT = "text"
SHORT_TEXT = "short-text"
RADIO = "radio"
SELECT = "select"
SELECT_IMAGE = "select_image"
SELECT_MULTIPLE = "select-multiple"
INTEGER = "integer"
FLOAT = "float"
DATE = "date"

QUESTION_TYPES = (
    (TEXT, _("text (multiple line)")),
    (SHORT_TEXT, _("short text (one line)")),
    (RADIO, _("radio")),
    (SELECT, _("select")),
    (SELECT_MULTIPLE, _("Select Multiple")),
    (SELECT_IMAGE, _("Select Image")),
    (INTEGER, _("integer")),
    (FLOAT, _("float")),
    (DATE, _("date")),
)

CHOICES_HELP_TEXT = _(
    """The choices field is only used if the question type
if the question type is 'radio', 'select', or
'select multiple' provide a comma-separated list of
options for this question ."""
)

INSPECTION_STATUS = (
    ('ready_to_start', 'Ready to start'),
    ('in_progress', 'In progress'),
    ('complete', 'Complete'),
)


class InspectionEntity(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='inspection/entity/logo/', blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inspection_entity', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class InspectionType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField( blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inspection_type', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Device(models.Model):
    entity = models.ForeignKey(InspectionEntity, on_delete=models.CASCADE, blank=True, null=True, related_name='device')
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.CASCADE, related_name='device', null=True, blank=True)
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='device_inspector', null=True, blank=True)
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='device_assigned_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_question_categories(self):
        categories = []
        for category in list(self.question_categories.order_by("id")):
            if category.questions.count() > 0:
                categories.append(category)
        return categories

class DeviceInspection(models.Model):
    title = models.CharField(max_length=256)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='device_inspection')
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='device_inspection', blank=True, null=True)
    start_datetime = models.DateTimeField(default=timezone.now) 
    pdf = models.FileField(upload_to='inspection/pdfs/', validators=[FileExtensionValidator(allowed_extensions=['pdf'])], blank=True, null=True)
    status = models.CharField(choices=INSPECTION_STATUS, default='ready_to_start', max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{} {}'.format(self.device.name, self.device.inspection_type)


    # def clean(self):
    #     super().clean()
    #     inspections = Inspection.objects.filter(device=self.device, start_datetime__month=timezone.now().month)
    #     if inspections.count() > 0:
    #         raise ValidationError('This ispection device already exist')

class Inspection(models.Model):
    entity = models.ForeignKey(InspectionEntity, on_delete=models.CASCADE, related_name='inspection', blank=True, null=True)
    devices = models.ManyToManyField(Device, related_name='inspection')
    inspectors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='inspection_inspectors')
    inspection_type = models.ForeignKey(InspectionType, on_delete=models.CASCADE, related_name='inspection', blank=True, null=True)
    start_date_time = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=50, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inspection_created_by', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(choices=INSPECTION_STATUS, default='ready_to_start', max_length=50)

    def __str__(self):
        return self.name

    def get_submit_report_url(self):
        device_inspections = []
        for device in self.devices.all():
            device_ins = device.device_inspection.all().first()
            if device_ins.status == 'complete':
                device_inspections.append(device_ins)
        if len(device_inspections) == len(self.devices.all()) :
            return reverse('inspection:inspection-report-create')
        return ''               


class InspectionReport(models.Model):
    inspection = models.ForeignKey(Inspection, on_delete=models.CASCADE,related_name='inspection_report', blank=True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inspection_report', blank=True, null=True)
    pdf = models.FileField(upload_to='inspection_report/pdfs/')
    is_active = models.BooleanField(default=True)
    reported_datetime = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     pass

class QuestionCategory(models.Model):
    entity = models.ForeignKey(InspectionEntity, on_delete=models.CASCADE, related_name='question_categories', blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='question_categories')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length = 250)
    description = models.TextField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='question_category', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Question Category"
        verbose_name_plural = "Question Categories"

    def __str__(self):
        return self.title

    def get_questions(self):
        return [x for x in list(self.questions.order_by("id"))]
    

class Question(models.Model):
    entity = models.ForeignKey(InspectionEntity, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    question_text = models.TextField()
    answer_type = models.CharField(choices=QUESTION_TYPES, max_length=50)
    choices = models.TextField(blank=True, null=True, help_text=CHOICES_HELP_TEXT)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='questions', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.question_text

    def save(self, *args, **kwargs):
        if self.answer_type in [RADIO, SELECT, SELECT_MULTIPLE]:
            self.validate_choices(self.choices)
        super(Question, self).save(*args, **kwargs)

    def validate_choices(self, choices):
        """Verifies that there is at least two choices in choices
        :param String choices: The string representing the user choices.
        """
        values = choices.split(settings.CHOICES_SEPARATOR)
        empty = 0
        for value in values:
            if value.replace(" ", "") == "":
                empty += 1
        if len(values) < 2 + empty:
            msg = "The selected field requires an associated list of choices."
            msg += " Choices must contain more than one item."
            raise ValidationError(msg)

    def get_clean_choices(self):
        """ Return split and stripped list of choices with no null values. """
        if self.choices is None:
            return []
        choices_list = []
        for choice in self.choices.split(settings.CHOICES_SEPARATOR):
            choice = choice.strip()
            if choice:
                choices_list.append(choice)
        return choices_list

    def get_choices(self):
        """
        Parse the choices field and return a tuple formatted appropriately
        for the 'choices' argument of a form widget.
        """
        choices_list = []
        for choice in self.get_clean_choices():
            choices_list.append((slugify(choice, allow_unicode=True), choice))
        choices_tuple = tuple(choices_list)
        return choices_tuple

class QuestionOption(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question_opyion_answer')
    option = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True) 

    def __str__(self):
        pass
    

class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer', blank=True, null=True)
    answer_type_text_number = models.TextField(blank=True, null=True)
    answer_type_boolean = models.BooleanField(blank=True, null=True)
    answer_type_image = models.ImageField(upload_to='inspections/question/answer/', blank=True, null=True)
    inspector = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='inspector_answer', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # def __str__(self):
    #     pass
    
    