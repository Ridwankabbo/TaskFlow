from celery import shared_task
from django.utils import timezone
from .models import Assignment
from ai.agent_logic import parse_assignment
from datetime import datetime

@shared_task
def process_assignment(assignment_id: int):
    try:
        assignment = Assignment.objects.get(id=assignment_id)
        assignment.status = 'processing'
        assignment.save()

        extracted = parse_assignment(assignment.raw_email)

        if extracted and extracted.get("title"):
            assignment.course = extracted.get("course", "Unknown")
            assignment.title = extracted.get("title", "Untitled")
            
            # Parse deadline
            if extracted.get("deadline"):
                try:
                    assignment.deadline = datetime.strptime(extracted["deadline"], "%Y-%m-%d %H:%M")
                except:
                    pass

            assignment.weight_marks = extracted.get("weight_marks")
            assignment.estimated_hours = extracted.get("estimated_hours")
            assignment.requirements = extracted.get("requirements", [])
            assignment.subtasks = extracted.get("subtasks", [])
            
            # Calculate Priority Score
            if assignment.deadline:
                days_left = max(1, (assignment.deadline - timezone.now()).days)
                marks = assignment.weight_marks or 50
                assignment.priority_score = int((marks * 10) / days_left)
            
            assignment.status = 'processed'
            assignment.processed_at = timezone.now()
        else:
            assignment.status = 'failed'

        assignment.save()
        return assignment.id

    except Exception as e:
        assignment.status = 'failed'
        assignment.save()
        return str(e)