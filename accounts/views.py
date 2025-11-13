from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseForbidden
from django.core.paginator import Paginator
from django.db.models import Q
from collections import Counter
import csv

from .forms import DailyLogForm
from .models import DailyLog

# ✅ Home Page
def home(request):

    return render(request, 'accounts/home.html')

from .forms import RegisterForm

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# ✅ Registration View
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if not all([username, email, password, confirm_password]):
            messages.error(request, 'All fields are required.')
            return render(request, 'accounts/register.html')

        if password != confirm_password:
            messages.error(request, 'Passwords do not match.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return render(request, 'accounts/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return render(request, 'accounts/register.html')

        user = User.objects.create_user(username=username, email=email, password=password)
        login(request, user)
        messages.success(request, 'Registration successful! You are now logged in.')
        return redirect('submit_log')

    return render(request, 'accounts/register.html')

# ✅ Login View
def custom_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('submit_log')
        else:
            messages.error(request, 'Login failed. Please register.')
            return redirect('register')
    return render(request, 'accounts/login.html')

from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def login_custom(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # Redirect based on role
            if user.is_staff:
                return redirect('mentor_dashboard')
            else:
                return redirect('user_logs')
        else:
            messages.error(request, 'Login failed. Please check credentials.')
            return redirect('login')

    return render(request, 'accounts/login.html')

# ✅ Logout View
def logout_view(request):
    logout(request)
    return redirect('login')

# ✅ Submit Log
@login_required
def submit_log(request):
    if request.method == 'POST':
        form = DailyLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = request.user
            log.save()
            return redirect('user_logs')
    else:
        form = DailyLogForm()
    return render(request, 'accounts/submit_log.html', {'form': form})

# ✅ View Logs
@login_required
def user_logs(request):
    logs = DailyLog.objects.filter(user=request.user).order_by('-created_at')

    # Pagination
    paginator = Paginator(logs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'accounts/user_logs.html', {
        'page_obj': page_obj,
        'logs': logs,  # in case your template still uses `logs`
    })

# ✅ Edit Log
@login_required
def edit_log(request, log_id):
    log = get_object_or_404(DailyLog, pk=log_id)
    if log.user != request.user:
        return HttpResponseForbidden("You are not allowed to edit this log.")

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=log)
        if form.is_valid():
            form.save()
            return redirect('user_logs')
    else:
        form = DailyLogForm(instance=log)

    return render(request, 'accounts/edit_log.html', {'form': form})

# ✅ Delete Log
@login_required
def delete_log(request, log_id):
    log = get_object_or_404(DailyLog, pk=log_id)
    if log.user != request.user:
        return HttpResponseForbidden("You are not allowed to delete this log.")

    if request.method == 'POST':
        log.delete()
        return redirect('user_logs')

    return render(request, 'accounts/delete_log.html', {'log': log})

from .models import Feedback, DailyLog
from .forms import FeedbackForm
from django.contrib.auth.decorators import login_required

@login_required
def add_feedback(request, log_id):
    log = get_object_or_404(DailyLog, pk=log_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.log = log
            feedback.mentor = request.user
            feedback.save()
            messages.success(request, 'Feedback added successfully.')
            return redirect('view_log', log_id=log_id)
    else:
        form = FeedbackForm()
    return render(request, 'accounts/add_feedback.html', {'form': form, 'log': log})

@login_required
def view_log(request, log_id):
    log = get_object_or_404(DailyLog, pk=log_id)
    feedbacks = log.feedbacks.all()
    return render(request, 'accounts/view_log.html', {'log': log, 'feedbacks': feedbacks})

from django.contrib.auth.decorators import user_passes_test
from .models import DailyLog

# ✅ View only for mentors (staff users)
@user_passes_test(lambda u: u.is_staff)
def mentor_dashboard(request):
    logs = DailyLog.objects.all().order_by('-created_at')
    return render(request, 'accounts/mentor_dashboard.html', {'logs': logs})


from django.contrib.auth.decorators import user_passes_test
from .models import DailyLog, Feedback
from .forms import FeedbackForm

@user_passes_test(lambda u: u.is_staff)
def give_feedback(request, log_id):
    log = get_object_or_404(DailyLog, id=log_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.mentor = request.user
            feedback.log = log
            feedback.save()
            return redirect('mentor_dashboard')
    else:
        form = FeedbackForm()

    return render(request, 'accounts/give_feedback.html', {'form': form, 'log': log})

from django.contrib.auth.decorators import login_required
from .models import Feedback

@login_required
def view_feedback(request):
    feedbacks = Feedback.objects.filter(log__user=request.user).select_related('log', 'mentor').order_by('-created_at')
    return render(request, 'accounts/view_feedback.html', {'feedbacks': feedbacks})
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.contrib import messages

def login_custom(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            # ✅ Redirect based on role
            if user.is_staff:
                return redirect('mentor_dashboard')  # Mentor
            else:
                return redirect('user_logs')  # Intern
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')

    return render(request, 'accounts/login.html')

@login_required
def view_log(request, log_id):
    log = get_object_or_404(DailyLog, id=log_id)
    feedbacks = log.feedbacks.all()
    return render(request, 'accounts/view_log.html', {'log': log, 'feedbacks': feedbacks})

@login_required
def add_feedback(request, log_id):
    log = get_object_or_404(DailyLog, id=log_id)
    if request.method == 'POST':
        comment = request.POST['comment']
        Feedback.objects.create(
            log=log,
            mentor=request.user,
            comment=comment
        )
        return redirect('view_log', log_id=log.id)
    return render(request, 'accounts/add_feedback.html', {'log': log})

@login_required
def view_feedback(request):
    feedbacks = Feedback.objects.filter(log__user=request.user).order_by('-created_at')
    return render(request, 'accounts/view_feedback.html', {'feedbacks': feedbacks})
from django.shortcuts import render

def home(request):
    return render(request, 'accounts/home.html')

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        messages.success(request, "Registration successful! Please login.")
        return redirect('login')
    return render(request, 'accounts/register.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Change 'home' to your dashboard view name if needed
        else:
            messages.error(request, "Invalid username or password")
            return redirect('login')
    return render(request, 'accounts/login.html')

from django.contrib.auth.decorators import login_required

@login_required
def my_feedbacks(request):
    feedbacks = Feedback.objects.filter(mentor=request.user).order_by('-created_at')
    return render(request, 'accounts/my_feedbacks.html', {'feedbacks': feedbacks})

from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from .models import DailyLog, Feedback
from .forms import FeedbackForm

@login_required
def add_feedback(request, log_id):
    log = get_object_or_404(DailyLog, id=log_id)

    # Optional: restrict to mentors by checking user role here if you have roles

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.log = log
            feedback.mentor = request.user
            feedback.save()
            return redirect('dashboard')  # Redirect where you want
    else:
        form = FeedbackForm()
    
    return render(request, 'accounts/add_feedback.html', {'form': form, 'log': log})

@login_required
def view_log(request, log_id):
    log = get_object_or_404(DailyLog, id=log_id)
    feedbacks = log.feedbacks.all()
    return render(request, 'accounts/view_log.html', {'log': log, 'feedbacks': feedbacks})
