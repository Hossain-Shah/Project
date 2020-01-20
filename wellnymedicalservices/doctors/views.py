from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .forms import DiagnosisForm, TODOItemForm
from .models import Diagnosis, TODOItem


class HomePageView(ListView):
    model = Diagnosis
    template_name = 'home.html'


class CreatePostView(CreateView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'post.html'
    success_url = reverse_lazy('doctors_diagnosis')


class CreatePost1View(CreateView):
    model = TODOItem
    form_class = TODOItemForm
    template_name = 'todolist.html'
    success_url = reverse_lazy('doctors_todolist')


class HomePage2View(ListView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'services.html'
    success_url = reverse_lazy('home')


class HomePage3View(ListView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'news.html'
    success_url = reverse_lazy('home')


class HomePage4View(ListView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'contact.html'
    success_url = reverse_lazy('home')


class HomePage1View(ListView):
    model = Diagnosis
    template_name = 'doctors_diagnosis.html'


class HomePage5View(ListView):
    model = TODOItem
    template_name = 'doctors_todolist.html'


