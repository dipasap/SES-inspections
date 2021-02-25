from django.shortcuts import render
from inspection.models import InspectionReport, DeviceInspection, Inspection
from inspection.forms import InspectionReportForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.filters import InspectionReportFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.utils import timezone
from inspection.utils import InspectionUtils

class InspectionReportListView(LoginRequiredMixin, ListView):
    model = InspectionReport

    def get_queryset(self):
        queryset = self.model.objects.all()
        filterd_queryset = InspectionReportFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs
    
    def get_template_names(self):
        return 'inspection/inspection_report/inspection_report_list.html'
        
class InspectionReportCreateView(LoginRequiredMixin, CreateView):
    model = InspectionReport
    template_name = "inspection/inspection_report/inspection_report_form.html"
    form_class = InspectionReportForm
    success_url = reverse_lazy('inspection:inspection-report-list')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)

    def post(self, request):
        device_inspection_ids = [int(pk) for pk in request.POST.getlist('ids[]')]
        inspection = Inspection.objects.get(pk=request.POST.get('inspection_id'))
        inspections_qs = DeviceInspection.objects.filter(pk__in=device_inspection_ids)
        pdf = InspectionUtils().merge_pdf(request=request, queryset=inspections_qs)
        if pdf:
            report = InspectionReport(inspection=inspection, user=request.user, pdf=pdf, is_active=False, reported_datetime=timezone.now())
            report.save()
            inspection.status = 'complete'
            inspection.save()
        return HttpResponseRedirect(reverse("inspection:dashboard"))

class InspectionReportUpdateView(LoginRequiredMixin, UpdateView):
    model = InspectionReport
    template_name = "inspection/inspection_report/inspection_report_form.html"
    form_class = InspectionReportForm
    success_url = reverse_lazy('inspection:inspection-report-list')

class InspectionReportDetailView(LoginRequiredMixin, DetailView):
    model = InspectionReport
    template_name = "inspection/inspection_report/inspection_report_details.html"

class InspectionReportDeleteView(LoginRequiredMixin, DeleteView):
    model = InspectionReport
    template_name = "inspection/inspection_report/inspection_report_delete.html"    
    success_url = reverse_lazy('inspection:inspection-report-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})