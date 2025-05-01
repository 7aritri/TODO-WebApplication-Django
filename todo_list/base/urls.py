from django.urls import path
from base.views import TaskList,TaskDetail,TaskCreate,TaskUpdate,DeleteView,CustomLoginView,RegisterPage,checkboxx
from django.contrib.auth import logout
from django.shortcuts import redirect
def custom_logout_view(request):
    logout(request)  # Logs out the user
    return redirect('login')

urlpatterns=[
	path("checkboxx/<int:pk>",checkboxx,name='checkboxx'),
	path("login/",CustomLoginView.as_view(),name="login"),
	path('logout/', custom_logout_view, name='admin-logout'),
	path("register/",RegisterPage.as_view(),name="register"),
	path('',TaskList.as_view(),name='tasks'),
	path('task/<int:pk>/',TaskDetail.as_view(),name='task'),
	path('task-create/',TaskCreate.as_view(),name='task-create'),
	path('task-update/<int:pk>/',TaskUpdate.as_view(),name='task-update'),
	path('task-delete/<int:pk>/',DeleteView.as_view(),name='task-delete')
]  