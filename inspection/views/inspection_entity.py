from django.shortcuts import render
from inspection.models import InspectionEntity
from inspection.forms import InspectionEntityForm, DeviceFormset, QuestionCategoryFormset, QuestionFormset
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.filters import InspectionEntityFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class InspectionEntityListView(LoginRequiredMixin, ListView):
    model = InspectionEntity
    template_name = "inspection/inspection_entity/inspection_entity_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        filterd_queryset = InspectionEntityFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs

class InspectionEntityCreateView(LoginRequiredMixin, CreateView):
    model = InspectionEntity
    template_name = "inspection/inspection_entity/inspection_entity_form.html"
    form_class = InspectionEntityForm
    success_url = reverse_lazy('inspection:inspection-entity-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class InspectionEntityUpdateView(LoginRequiredMixin, UpdateView):
    model = InspectionEntity
    template_name = "inspection/inspection_entity/inspection_entity_form.html"
    form_class = InspectionEntityForm
    success_url = reverse_lazy('inspection:inspection-entity-list')

class InspectionEntityDetailView(LoginRequiredMixin, DetailView):
    model = InspectionEntity
    template_name = "inspection/inspection_entity/inspection_entity_details.html"

class InspectionEntityDeleteView(LoginRequiredMixin, DeleteView):
    model = InspectionEntity
    template_name = "inspection/inspection_entity/inspection_entity_delete.html"    
    success_url = reverse_lazy('inspection:inspection-entity-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})


# class InspectionEntityCreateView(LoginRequiredMixin, CreateView):
#     model = InspectionEntity
#     template_name = "inspection/inspection_entity/inspection_entity_form.html"
#     form_class = InspectionEntityForm
#     success_url = reverse_lazy('inspection:inspection-entity-list')

#     def get_context_data(self, **kwargs):
#         context = super(InspectionEntityCreateView, self).get_context_data(**kwargs)
#         if self.request.POST:
#             context['device_formset'] = DeviceFormset(self.request.POST)
#             context['question_category_formset'] = QuestionCategoryFormset(self.request.POST)
#             context['question_formset'] = QuestionFormset(self.request.POST)
#         else:
#             context['device_formset'] = DeviceFormset()
#             context['question_category_formset'] = QuestionCategoryFormset()
#             context['question_formset'] = QuestionFormset()
#         return context

#     def form_valid(self, form):
#         context = self.get_context_data()
#         form.instance.created_by = self.request.user
#         device_formset = context['device_formset']
#         question_category_formset = context['question_category_formset']
#         question_formset = context['question_formset']
#         import pdb; pdb.set_trace()
#         self.object = form.save()

#         if device_formset.is_valid():
#             pass

#         if question_category_formset.is_valid():
#             pass

#         if question_formset.is_valid():
#             pass

#         return super().form_valid(form)
