import os
from celery import Celery

# Django-র ডিফল্ট সেটিংস মডিউল সেট করা
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'TaskFlow.settings')

# Celery অ্যাপ তৈরি করা
app = Celery('Taskflow')

# Django settings ফাইল থেকে Celery কনফিগারেশন লোড করা
# 'CELERY_' প্রিফিক্স থাকা কনফিগগুলো এটা রিড করবে
app.config_from_object('django.conf:settings', namespace='CELERY')

# সব রেজিস্টার্ড Django অ্যাপের ভেতর থেকে টাস্ক (tasks.py) স্বয়ংক্রিয়ভাবে খুঁজে নেওয়া
app.autodiscover_tasks()
