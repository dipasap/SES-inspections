from django.shortcuts import render
from inspection.models import QuestionCategory
from inspection.forms import QuestionCategoryForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.filters import QuestionCategoryFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class QuestionCategoryListView(LoginRequiredMixin, ListView):
    model = QuestionCategory

    def get_queryset(self):
        if self.request.is_ajax():
            queryset = self.model.objects.all()
            filterd_queryset = QuestionCategoryFilter(self.request.GET, queryset=queryset)
            return filterd_queryset.qs 

        queryset = self.model.objects.all()
        filterd_queryset = QuestionCategoryFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs

    def get_template_names(self):
        if self.request.is_ajax():
            return 'inspection/partials/dropdown-list.html'
        return 'inspection/question_category/question_category_list.html'

class QuestionCategoryCreateView(LoginRequiredMixin, CreateView):
    model = QuestionCategory
    template_name = "inspection/question_category/question_category_form.html"
    form_class = QuestionCategoryForm
    success_url = reverse_lazy('inspection:question-category-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class QuestionCategoryUpdateView(LoginRequiredMixin, UpdateView):
    model = QuestionCategory
    template_name = "inspection/question_category/question_category_form.html"
    form_class = QuestionCategoryForm
    success_url = reverse_lazy('inspection:question-category-list')

class QuestionCategoryDetailView(LoginRequiredMixin, DetailView):
    model = QuestionCategory
    template_name = "inspection/question_category/question_category_details.html"

class QuestionCategoryDeleteView(LoginRequiredMixin, DeleteView):
    model = QuestionCategory
    template_name = "inspection/question_category/question_category_delete.html"    
    success_url = reverse_lazy('inspection:question-category-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})