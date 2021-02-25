from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from inspection.models import Question
from inspection.forms import QuestionForm
from inspection.filters import QuestionFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

class QuestionListView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "inspection/question/question_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        filterd_queryset = QuestionFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs

class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    template_name = "inspection/question/question_form.html"
    form_class = QuestionForm
    success_url = reverse_lazy('inspection:question-list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)

class QuestionUpdateView(LoginRequiredMixin, UpdateView):
    model = Question
    template_name = "inspection/question/question_form.html"
    form_class = QuestionForm
    success_url = reverse_lazy('inspection:inspection-type-list')

class QuestionDetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "inspection/question/question_details.html"

class QuestionDeleteView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "inspection/question/question_delete.html"    
    success_url = reverse_lazy('inspection:inspection-type-list')

    def get(self, request, *args, **kwargs):
        record = self.get_object()
        return render(request, self.template_name, {'record': record})
