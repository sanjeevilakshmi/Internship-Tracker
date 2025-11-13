# accounts/models.py
from django.db import models
from django.contrib.auth.models import User

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    task_title = models.CharField(max_length=200)
    task_description = models.TextField()
    status = models.CharField(max_length=20, choices=[
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.task_title}"

class Feedback(models.Model):
    log = models.ForeignKey(DailyLog, on_delete=models.CASCADE, related_name='feedbacks')
    mentor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mentor_feedbacks')
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.mentor.username} on {self.log.task_title}"

