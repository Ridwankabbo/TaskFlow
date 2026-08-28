from assigment.tasks import process_assignment   # note: your app name is "assigment"
from assigment.models import Assignment
from django.contrib.auth import get_user_model
import datetime
from django.utils import timezone
User = get_user_model()
user = User.objects.first()   # or your test user

test_email = """
Subject: Final Project Submission - CSE-4101

Dear Students,

Please submit your project titled "AI-Based Smart Attendance System" by 20 September 2026 at 11:59 PM.

This assignment is worth 40 marks.
Estimated time required: 15 hours.

Requirements:
1. Use Django REST Framework + React
2. Implement face recognition
3. Deploy on a cloud platform

Subtasks:
- Database Design (due in 4 days)
- Backend API (due in 8 days)
- Frontend Integration (due in 12 days)

Best regards,
Prof. Karim
"""

assign = Assignment.objects.create(
    user=user,
    raw_email=test_email,
    course="Test Course",
    title="Test Title",
    deadline=timezone.now() + datetime.timedelta(days=7),
    status='pending'
)

print("Assignment ID:", assign.id)
process_assignment.delay(assign.id)