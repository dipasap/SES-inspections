from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Inspection, Device, DeviceInspection
from .utils import InspectionUtils
from django.core.files import File
from io import BytesIO
from django.utils import timezone
from django.http import HttpResponse

# @receiver(post_save, sender=Inspection)
# def create_and_save_pdf(sender, instance, created, **kwargs):
#     if created:
#         template_name = 'inspection/utils/render_pdf.html'
#         pdf = InspectionUtils().render_to_pdf(template_name, {'inspection':instance})
#         if pdf:
#             filename = 'inspection_%s.pdf' % (timezone.now().timestamp())
#             content = "attachment; filename=%s " % (filename)
#             receipt_file = BytesIO(pdf.content)
#             instance.pdf = File(receipt_file, filename)
#             instance.save()

@receiver(post_save, sender=Device)
def add_inspection(sender, instance, created, **kwargs):
	if created:
		inspection = DeviceInspection(
				title = "%s-%s" % (instance.name, instance.inspection_type.name),
				device = instance,
				inspector = instance.inspector
			)
		inspection.save()
	