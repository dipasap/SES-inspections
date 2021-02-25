from django.shortcuts import render
from inspection.models import Device
from inspection.forms import DeviceForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.filters import DeviceFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class DeviceListView(LoginRequiredMixin, ListView):
    model = Device

    def get_queryset(self):
        
        if self.request.is_ajax():
            queryset = self.model.objects.all()
            filterd_queryset = DeviceFilter(self.request.GET, queryset=queryset)
            return filterd_queryset.qs 

        queryset = self.model.objects.all()
        filterd_queryset = DeviceFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs
    
    def get_template_names(self):
        if self.request.is_ajax():
            return 'inspection/partials/dropdown-list.html'
        return 'inspection/inspection_device/inspection_device_list.html'
        
class DeviceCreateView(LoginRequiredMixin, CreateView):
    model = Device
    template_name = "inspection/inspection_device/inspection_device_form.html"
    form_class = DeviceForm
    success_url = reverse_lazy('inspection:inspection-device-list')

    def form_valid(self, form):
        form.instance.assigned_by = self.request.user
        return super().form_valid(form)

class DeviceUpdateView(LoginRequiredMixin, UpdateView):
    model = Device
    template_name = "inspection/inspection_device/inspection_device_form.html"
    form_class = DeviceForm
    success_url = reverse_lazy('inspection:inspection-device-list')

class DeviceDetailView(LoginRequiredMixin, DetailView):
    model = Device
    template_name = "inspection/inspection_device/inspection_device_details.html"

class DeviceDeleteView(LoginRequiredMixin, DeleteView):
    model = Device
    template_name = "inspection/inspection_device/inspection_device_delete.html"    
    success_url = reverse_lazy('inspection:inspection-device-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})