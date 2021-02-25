from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from users.models import CustomUser
from users.forms import CustomUserForm
from users.filters import CustomUserFilter
from django.views.generic import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView

class CustomUserListView(LoginRequiredMixin, ListView):
    model = CustomUser
    template_name = "users/user_list.html"

    def get_queryset(self):
        queryset = self.model.objects.all()
        filterd_queryset = CustomUserFilter(self.request.GET, queryset=queryset)
        return filterd_queryset.qs

class CustomUserCreateView(LoginRequiredMixin, CreateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = CustomUserForm
    success_url = reverse_lazy('users:user-list')

class CustomUserUpdateView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    template_name = "users/user_form.html"
    form_class = CustomUserForm
    success_url = reverse_lazy('users:user-list')

class CustomUserDetailView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = "users/user_details.html"