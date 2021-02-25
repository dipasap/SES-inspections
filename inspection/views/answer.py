from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.views.generic.edit import CreateView
from inspection.inspector_forms import InspectionQuestioAnswerForm
from inspection.models import Answer, Device
from django.urls import reverse
from inspection.utils import InspectionUtils
from io import BytesIO
from django.utils import timezone
from django.core.files import File


class InspectionQuestioAnswerView(LoginRequiredMixin, View):
    template_name = 'inspection/inspection/inspector/inspection_device_question_answer.html'

    def get(self, request, *args, **kwargs):
        device = Device.objects.get(pk=int(kwargs.get('pk')))
        step_no = kwargs.get("step", 0)
        inspection_name = kwargs.get("inspection_name", 0)
        forms = InspectionQuestioAnswerForm(inspection_name=kwargs.get('inspection_name'), device=device, user=request.user, step=step_no)
        categories = forms.current_categories
        context = {
            'forms':forms,
            'categories': categories,
            'inspection_name': inspection_name,
            'device': device.name,
            'pk': device.pk,
            'step': step_no,
            'kwargs': kwargs
        }

        device_ins = device.device_inspection.all().first()
        device_ins.status = 'in_progress'
        device_ins.inspector = request.user
        device_ins.save()
        
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        device = Device.objects.get(pk=int(kwargs.get('pk')))
        step = kwargs.get("step", 0)
        forms = InspectionQuestioAnswerForm(request.POST ,inspection_name=kwargs.get('inspection_name'), device=device, user=request.user, step=step)
        categories = forms.current_categories
        
        context = {"forms": forms, "device": device, "categories": categories}
        if forms.is_valid():
            return self.treat_valid_form(forms, kwargs, request, device)
        return self.handle_invalid_form(context, forms, request, device)

    def handle_invalid_form(self, context, form, request, survey):
        # LOGGER.info("Non valid form: <%s>", form)
        return render(request, self.template_name, context)

    def treat_valid_form(self, form, kwargs, request, device):
        session_key = "device_%s" % (kwargs["pk"],)
        if session_key not in request.session:
            request.session[session_key] = {}
        for key, value in list(form.cleaned_data.items()):
            request.session[session_key][key] = value
            request.session.modified = True
        next_url = form.next_step_url()
        response = None
        
        # when it's the last step
        if not form.has_next_step():
            save_form = InspectionQuestioAnswerForm(request.session[session_key], inspection_name=kwargs["inspection_name"], device=device, user=request.user)
            if save_form.is_valid():
                response = save_form.save()
            else:
                LOGGER.warning("A step of the multipage form failed but should have been discovered before.")
        # if there is a next step
        
        if next_url is not None:
            return redirect(next_url)
        del request.session[session_key]

        if response is None:
            return redirect(reverse("inspection:dashboard"))
        
        next_ = request.session.get("next", None)

        if next_ is not None:
            if "next" in request.session:
                del request.session["next"]
            return redirect(next_)

        self.create_and_save_pdf(device)
        inspection_id = device.inspection.filter(inspection_type=device.inspection_type).first().id
        return redirect(reverse("inspection:inspection-details", kwargs={'pk':inspection_id}))

    def create_and_save_pdf(self, device):
        template_name = 'inspection/utils/render_pdf.html'
        import pdb; pdb.set_trace()
        protocal = 'https://' if self.request.is_secure() else 'http://'
        entity_logo = protocal+''+self.request.get_host()+''+device.entity.logo.url
        pdf = InspectionUtils.render_to_pdf(self, template_name, context_dict={'device':device, 'entity_logo':entity_logo})
        if pdf:
            filename = 'inspection_%s.pdf' % (timezone.now().timestamp())
            content = "attachment; filename=%s " % (filename)
            receipt_file = BytesIO(pdf.content)
            data = device.device_inspection.all().first()
            # import pdb; pdb.set_trace()
            device_inspection = device.device_inspection.all().first()
            device_inspection.pdf = File(receipt_file, filename)
            device_inspection.status = 'complete'
            device_inspection.save()
            return True

