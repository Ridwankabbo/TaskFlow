from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Assignment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    raw_email = models.TextField()
    course = models.CharField(max_length=200)
    title = models.CharField(max_length=500)
    deadline = models.DateTimeField()
    weight_marks = models.IntegerField(null=True, blank=True)
    priority_score = models.IntegerField(default=0)
    estimated_hours = models.IntegerField(null=True, blank=True)
    requirements = models.JSONField(default=list)
    subtasks = models.JSONField(default=list)
    status = models.CharField(max_length=50, default='pending')  # pending, processed, failed
    created_at = models.DateTimeField(auto_now_add=True)
    processed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.course} - {self.title}"
    
    class Meta:
        ordering = ['-created_at']