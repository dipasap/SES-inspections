from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.models import InspectionType
from inspection.forms import InspectionTypeForm
from inspection.filters import InspectionTypeFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class InspectionTypeListView(LoginRequiredMixin, ListView):
    model = InspectionType
    template_name = "inspection/inspection_type/inspection_type_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        filterd_queryset = InspectionTypeFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs

class InspectionTypeCreateView(LoginRequiredMixin, CreateView):
    model = InspectionType
    template_name = "inspection/inspection_type/inspection_type_form.html"
    form_class = InspectionTypeForm
    success_url = reverse_lazy('inspection:inspection-type-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class InspectionTypeUpdateView(LoginRequiredMixin, UpdateView):
    model = InspectionType
    template_name = "inspection/inspection_type/inspection_type_form.html"
    form_class = InspectionTypeForm
    success_url = reverse_lazy('inspection:inspection-type-list')

class InspectionTypeDetailView(LoginRequiredMixin, DetailView):
    model = InspectionType
    template_name = "inspection/inspection_type/inspection_type_details.html"

class InspectionTypeDeleteView(LoginRequiredMixin, DeleteView):
    model = InspectionType
    template_name = "inspection/inspection_type/inspection_type_delete.html"    
    success_url = reverse_lazy('inspection:inspection-type-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})
