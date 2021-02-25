from io import BytesIO
from xhtml2pdf import pisa
from django.template.loader import get_template
from django.http import HttpResponse, FileResponse
from PyPDF2 import PdfFileMerger, PdfFileReader
from django.utils import timezone
from io import BytesIO
from django.core.files import File

class InspectionUtils():
    """
        Utils Is helper class which will give you some methods to inhence the codes
        1) render_to_pdf -> return pdf
    """

    def render_to_pdf(self, template_src, context_dict={}):
        template = get_template(template_src)
        html  = template.render(context_dict)
        result = BytesIO()
        pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
        if not pdf.err:
            return HttpResponse(result.getvalue(), content_type='application/pdf')
        return None

    def merge_pdf(self, request, queryset):
        merged_pdf_object = PdfFileMerger()
        for inspection in queryset:
            merged_pdf_object.append(PdfFileReader(inspection.pdf))
        filestream = BytesIO()
        merged_pdf_object.write(filestream)
        merged_pdf_object.close()
        filestream.seek(0)
        filename = "inspection_reprt_%s.pdf" %((timezone.now().timestamp()))
        return File(filestream, filename)
