from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from base.models import Task
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
# Create your views here.


class CustomLoginView(LoginView):
	template_name="base/login.html"
	fields="__all__"
	content_object_name='login'
	redirect_authenticated_user= True
	def get_success_url(self):
		return reverse_lazy("tasks")

class RegisterPage(FormView):
	template_name='base/register.html'
	form_class = UserCreationForm
	redirect_authenticated_user=True
	success_url=reverse_lazy('tasks')
	def form_valid(self,form):
		user=form.save()
		print("ok")
		if user is not None:
			login(self.request,user)
		return super(RegisterPage,self).form_valid(form)
	def get(self,*args,**kwargs):
		if self.request.user.is_authenticated:
			login(self.request,user)
		return super(RegisterPage,self).get(*args,**kwargs)

class TaskList(LoginRequiredMixin,ListView):
	model= Task
	content_object_name='tasks'
	def get_context_data(self,**kwargs):
		context=super().get_context_data(**kwargs)
		m=self.model.objects.filter(user=self.request.user,complete=False)
		context['object_list']=m
		count=m.count()
		search_input= self.request.GET.get('search-area') or ''
		if search_input:
			m=self.model.objects.filter(title__startswith=search_input)
			context['object_list']=m
		context['search_input']=search_input
		context['count']=count
		print(context)

		return context

class TaskDetail(LoginRequiredMixin,DetailView):
	model=Task	
	success_url=reverse_lazy("tasks")

class TaskCreate(LoginRequiredMixin,CreateView):
	model=Task
	fields=['title','description','complete']
	success_url=reverse_lazy("tasks")
	def form_valid(self,form):
		form.instance.user=self.request.user
		return super(TaskCreate,self).form_valid(form)
class TaskUpdate(LoginRequiredMixin,UpdateView):
	model=Task 
	fields=['title','description','complete']

	success_url=reverse_lazy("tasks")

class DeleteView(LoginRequiredMixin,DeleteView):
	model=Task
	content_object_name='task'
	success_url=reverse_lazy('tasks')
def checkboxx(request, pk):
    # Get the object by its primary key (pk)
    obj = Task.objects.get(pk=pk)
    
    # Toggle the value of is_active
    obj.complete= not obj.complete
    obj.save()  # Save the updated model to the database
    
    # Redirect back to the page or another page
    return redirect('tasks')