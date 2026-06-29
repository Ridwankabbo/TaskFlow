from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Assignment
from .serializers import AssignmentSerializer
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AssigmentViewSet(viewsets.ModelViewSet):
    
    permission_classes = [IsAuthenticated]
    serializer_class = AssignmentSerializer
    queryset = Assignment.objects.all()
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        raw_email = request.data.get('email_content') or request.data.get('raw_email')
        if not raw_email:
            return Response({"error": "Email content required"}, status=400)
        
        assignment = Assignment.objects.create(
            user=request.user,
            raw_email=raw_email,
            status='pending'
        )
        
        # Trigger background task
        process_assignment.delay(assignment.id)
        
        serializer = self.get_serializer(assignment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
