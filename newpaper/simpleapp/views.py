from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView, DeleteView
from news.models import Post, Category, Author
from django.core.paginator import Paginator
from .filters import NewFilter
from simpleapp.forms import NewForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from datetime import datetime
from appointments.models import Appointment
from appointments.views import AppointmentView
from django.core.mail import send_mass_mail
from django.core.cache import cache

class NewList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-datepost']
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewFilter(self.request.GET,queryset=self.get_queryset())
        return context

class NewDetailView(DetailView):
    template_name = 'new.html'
    queryset = Post.objects.all()
    context_object_name = 'news'

    def get_object(self, *args, **kwargs): # переопределяем метод получения объекта, как ни странно
        obj = cache.get(self.kwargs["pk"], None) # кэш очень похож на словарь, и метод get действует также. Он забирает значение по ключу, если его нет, то забирает None.
 
        # если объекта нет в кэше, то получаем его и записываем в кэш
        if not obj:
            obj = super().get_object(queryset=self.queryset) 
            cache.set(self.kwargs["pk"], obj)
        
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category = self.get_object(self.queryset).get_category()
        context['is_not_subs'] = not Appointment.objects.all().filter(subscribers=category).exists()
        return context

@login_required
def subs(request):
    user = request.user
    category = request.POST.get("categoryname")
    categoryname = Category.objects.get(categoryname=category)
    if not Appointment.objects.get(user=user):
        subs = Appointment(user=user)
        subs.save()
    else:
        subs = Appointment.objects.get(user=user)
        subs.subscribers.add(categoryname)
    return redirect("/")

class NewsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewFilter(self.request.GET,queryset=self.get_queryset())
        return context
    
class NewUpdateView(PermissionRequiredMixin, CreateView):
    template_name = 'new_create.html'
    permission_required = ('news.change_post',)
    form_class = NewForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)
    
class NewDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'new_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'
    context_object_name = 'news'

class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')

class AddPost(PermissionRequiredMixin, CreateView):
    queryset = Post.objects.all()
    template_name = 'new_create.html'
    permission_required = ('news.add_post',)
    form_class = NewForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = NewFilter(self.request.GET, queryset=self.get_queryset())
        context['form'] = NewForm()
        return context































