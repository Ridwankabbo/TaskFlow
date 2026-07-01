from django.test import TestCase
from .tasks import process_assignment
from .models import Assignment
# Create your tests here.

assign = Assignment.objects.create(user='user1@gmail.com', raw_email="Your test email text here...")
process_assignment.delay(assign.id)
