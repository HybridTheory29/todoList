from django.contrib.auth import authenticate, login as user_login, logout as user_logout
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.template.context_processors import request
from django.views.generic.list import  ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from django.utils.timezone import localtime

from main.models import *
from main.forms import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response

class OverdueTasksAPIView(APIView):
    def get(self, request):
        tasks = Task.objects.filter(complete=False, deadline__lt=timezone.now())
        data = [{"title": task.title, "deadline": task.deadline} for task in tasks]
        return Response(data)

def login_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')

        usr = authenticate(request, username=login, password=password)
        if usr is not None:
            user_login(request, usr)
            return HttpResponseRedirect('/')
        else:
            return render(request, 'main/login_form.html')

    return render(request, 'main/login_form.html')

def reg_view(request):
    if request.method == 'POST':
        login = request.POST.get('login')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password == password2:
            User.objects.create_user(login, password=password)
            usr = authenticate(request, username=login, password=password)
            if usr is not None:
                user_login(request, usr)
                return HttpResponseRedirect('/')
            else:
                return render(request, 'main/login_form.html')

    return render(request, 'main/reg_form.html')

def logout_view(request):
    user_logout(request)
    return HttpResponseRedirect('/login')

def user_profile(request, username):
    user = User.objects.get(username=username)
    context = {"user": user}

    return render(request, 'main/user_profile.html', context)

class CategoryList(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'main/lists.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        
        if search_input:
            context['categories'] = context['categories'].filter(name__startswith=search_input)

        context['search_input'] = search_input

        return context

class CategoryTasks(ListView):
    model = Task
    template_name = 'main/task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        category = Category.objects.get(pk=self.kwargs['pk'])
        return Task.objects.filter(category=category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['pk'])
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get('search-area') or ''
        
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context
     
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'main/task_form.html'
    fields = ['title', 'description', 'deadline']

    def form_valid(self, form):
        category = Category.objects.get(pk=self.kwargs['category_id'])
        form.instance.category = category
        form.instance.user = self.request.user
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.get(pk=self.kwargs['category_id'])
        context['now'] = timezone.now()
        return context

    def get_success_url(self):
        return reverse_lazy('category_tasks', kwargs={'pk': self.kwargs['category_id']})

class CategoryCreate(LoginRequiredMixin, CreateView):
    model = Category
    fields = ['name']
    success_url = reverse_lazy('category-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(CategoryCreate, self).form_valid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'main/category_form.html'
    fields = ['name']

    success_url = reverse_lazy('category-list')

class TaskUpdateView(UpdateView):
    model = Task
    template_name = 'main/task_form.html'
    fields = ['title', 'description', 'deadline']

    def form_valid(self, form):
        task = form.save(commit=False)
        task.category = get_object_or_404(Category, pk=self.kwargs['category_id'])
        task.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = get_object_or_404(Category, pk=self.kwargs['category_id'])
        return context

    def get_success_url(self):
        return reverse_lazy('category_tasks', kwargs={'pk': self.kwargs['category_id']})

class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'main/task_confirm_delete.html'

    def get_success_url(self):
        return reverse_lazy('category_tasks', kwargs={'pk': self.object.category.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object.category
        return context
    
class CategoryDelete(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'main/category_confirm_delete.html'
    success_url = reverse_lazy('category-list')

def category_important(request, pk):
    category = get_object_or_404(Category, pk=pk, user=request.user)
    category.important = not category.important
    category.save()

    return redirect('category-list')

def task_important(request, category_id, pk):
    task = get_object_or_404(Task, pk=pk, category_id=category_id)
    task.important = not task.important
    task.save()

    return redirect(reverse('category_tasks', kwargs={'pk': category_id}))

def task_complete(request, category_id, pk):
    task = get_object_or_404(Task, pk=pk, category_id=category_id)
    task.complete = not task.complete
    task.save()

    return redirect(reverse('category_tasks', kwargs={'pk': category_id}))