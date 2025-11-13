"""internship_tracker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  # ✅ include is required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # ✅ Add this line
]

from django.contrib import admin
from accounts import views  # ✅ Import views from accounts app
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # ✅ This includes login/logout/etc.
    path('submit-log/', views.submit_log, name='submit_log'),
    path('logs/', views.user_logs, name='user_logs'),
    path('logs/edit/<int:log_id>/', views.edit_log, name='edit_log'),
    path('logs/delete/<int:log_id>/', views.delete_log, name='delete_log'),
]

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', LoginView.as_view(template_name='accounts/login.html'), name='login'),  # 👈 Login is homepage
    path('', include('accounts.urls')),
]
