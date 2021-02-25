from django.shortcuts import render
from inspection.models import Inspection
from inspection.forms import InspectionForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.filters import InspectionFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class InspectionListView(LoginRequiredMixin, ListView):
    model = Inspection

    def get_queryset(self):
        
        if self.request.is_ajax():
            queryset = self.model.objects.all()
            filterd_queryset = InspectionFilter(self.request.GET, queryset=queryset)
            return filterd_queryset.qs 

        queryset = self.model.objects.all()
        filterd_queryset = InspectionFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs
    
    def get_template_names(self):
        if self.request.is_ajax():
            return 'inspection/partials/dropdown-list.html'
        return 'inspection/inspection/inspection_list.html'
        
class InspectionCreateView(LoginRequiredMixin, CreateView):
    model = Inspection
    template_name = "inspection/inspection/inspection_form.html"
    form_class = InspectionForm
    success_url = reverse_lazy('inspection:inspection-list')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)

class InspectionUpdateView(LoginRequiredMixin, UpdateView):
    model = Inspection
    template_name = "inspection/inspection/inspection_form.html"
    form_class = InspectionForm
    success_url = reverse_lazy('inspection:inspection-list')

class InspectionDetailView(LoginRequiredMixin, DetailView):
    model = Inspection

    def get_context_data(self, **kwargs):
        context = super(InspectionDetailView, self).get_context_data(**kwargs)
        device_inspection_list = []
        for device in context['object'].devices.all():
            device_inspection_list.append(device.device_inspection.all().first())
        
        if self.object.status == 'ready_to_start':
            self.object.status = 'in_progress'
            self.object.save()
            
        context['ids'] = [pk.id for pk in device_inspection_list]
        return context
    
    def get_template_names(self):
        if self.request.user.is_inspector:
            return "inspection/inspection/inspector/inspection_details_devices.html"
        return "inspection/inspection/inspection_details.html"

class InspectionDeleteView(LoginRequiredMixin, DeleteView):
    model = Inspection
    template_name = "inspection/inspection/inspection_delete.html"    
    success_url = reverse_lazy('inspection:inspection-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})