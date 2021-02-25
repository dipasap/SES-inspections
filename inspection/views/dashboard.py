from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from inspection.models import Inspection

class Dashboard(LoginRequiredMixin, TemplateView):

    def get_context_data(self, **kwargs):
        context = super(Dashboard, self).get_context_data(**kwargs)
        if self.request.user.is_inspector:
            context['inspections'] = Inspection.objects.filter(inspectors=self.request.user, status= 'ready_to_start')
            context['in_progress_inspections'] = Inspection.objects.filter(inspectors=self.request.user, status= 'in_progress')
            context['archive_inspections'] = Inspection.objects.filter(inspectors=self.request.user, status= 'complete')
        return context

    def get_template_names(self):
        if self.request.user.is_admin:
            return 'inspection/dashboard/admin.html'
        return 'inspection/dashboard/inspector.html'