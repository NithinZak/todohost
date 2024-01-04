from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView,DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from .models import Tasks
from django.shortcuts import redirect

from django.contrib.auth.views import LoginView,LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    success_url = 'tasks'
    # def get_success_url(self):
    #     return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)
    
class Logout(LogoutView):
    success_url = reverse_lazy('login')


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Tasks
    fields = ['task', 'completed','description']
    success_url = reverse_lazy('tasks')
    template_name = 'taskcreate.html'

    def form_valid(self, form):
        form.instance.users = self.request.user
        return super().form_valid(form)

class TaskList(LoginRequiredMixin,ListView):
    model = Tasks
    context_object_name = 'tasks'
    template_name = 'tasklist.html'
    def get_queryset(self):
        return Tasks.objects.filter(users=self.request.user)

class TaskDetailView(DetailView):
    model = Tasks
    template_name = 'taskdetail.html'
    def get(self,request,pk):
        obj = Tasks.objects.get(pk=pk)
        return render(request,self.template_name,{'tasks':obj})

def TaskCompleted(request, id):
    obj = Tasks.objects.get(id=id)
    obj.completed = True
    obj.save()
    return render(request,'tasklist.html')
    
class TaskUpdate(UpdateView):
    model = Tasks
    fields = ['task', 'completed','description']
    success_url = reverse_lazy('tasks')
    template_name = 'taskcreate.html'


class TaskDeleteView(DeleteView):
    model = Tasks
    template_name = 'taskdelete.html'
    success_url = reverse_lazy('tasks')
