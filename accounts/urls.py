from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

from django.contrib.auth.views import LoginView

urlpatterns = [

    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('submit-log/', views.submit_log, name='submit_log'),
    path('logs/', views.user_logs, name='user_logs'),
]
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('submit-log/', views.submit_log, name='submit_log'),
    path('logs/', views.user_logs, name='user_logs'),
    path('logs/edit/<int:log_id>/', views.edit_log, name='edit_log'),
    path('logs/delete/<int:log_id>/', views.delete_log, name='delete_log'),
]

from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # 👈 homepage
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    # Add other paths like register, etc.
]

from django.contrib.auth.views import LoginView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
]

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
]

from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import path
from . import views

class CustomLoginView(LoginView):
    template_name = 'accounts/login.html'

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password.')
        return super().form_invalid(form)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
]


from django.urls import path
from . import views

urlpatterns = [
    path('', views.custom_login, name='login'),  # Start with login
    path('register/', views.register, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('submit-log/', views.submit_log, name='submit_log'),
    path('logs/', views.user_logs, name='user_logs'),
    path('logs/edit/<int:log_id>/', views.edit_log, name='edit_log'),
    path('logs/delete/<int:log_id>/', views.delete_log, name='delete_log'),
    path('mentor-dashboard/', views.mentor_dashboard, name='mentor_dashboard'),
    path('logs/<int:log_id>/feedback/', views.give_feedback, name='give_feedback'),
    path('my-feedback/', views.view_feedback, name='view_feedback'),
    # accounts/urls.py
    path('login/', views.login_custom, name='login'),
    path('log/<int:log_id>/add-feedback/', views.add_feedback, name='add_feedback'),
    path('my-feedbacks/', views.my_feedbacks, name='my_feedbacks'),
    path('log/<int:log_id>/add-feedback/', views.add_feedback, name='add_feedback'),
    path('log/<int:log_id>/', views.view_log, name='view_log')

]
