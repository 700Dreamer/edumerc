import os
import django
from datetime import datetime, timedelta, time

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from educoach.models import Coach, CoachingSession
from payments.models import Withdrawal
from rest_framework.test import APIRequestFactory, force_authenticate
from educoach.views import CoachViewSet
from django.db.models.signals import post_save

User = get_user_model()
factory = APIRequestFactory()

def run_tests():
    # Disconnect notification signals to prevent Email API failures during test
    try:
        from notifications.signals import session_notification_signal
        post_save.disconnect(session_notification_signal, sender=CoachingSession)
    except ImportError:
        pass
    print("--- Testing Coach Earnings Endpoint ---")
    
    # 1. Setup Test Coach
    teacher, _ = User.objects.get_or_create(username='earning_coach', email='ec@test.com', role='TEACHER', is_coach=True)
    coach, _ = Coach.objects.get_or_create(user=teacher, defaults={'title': 'Math Expert', 'price_per_hour': 100})
    
    # 2. Setup Test Student
    student, _ = User.objects.get_or_create(username='paying_student', email='ps@test.com', role='STUDENT')
    
    # Clear existing data for this coach
    CoachingSession.objects.filter(coach=coach).delete()
    Withdrawal.objects.filter(user=teacher).delete()
    
    # 3. Create Scenarios
    
    # A. Completed Session (Demanding)
    CoachingSession.objects.create(
        coach=coach, student=student, date=datetime.now().date() - timedelta(days=1),
        start_time=time(9, 0), end_time=time(10, 0), duration=1, total_price=100.00,
        status='completed'
    )
    
    # B. Confirmed Future Session (Expecting)
    CoachingSession.objects.create(
        coach=coach, student=student, date=datetime.now().date() + timedelta(days=1),
        start_time=time(10, 0), end_time=time(11, 0), duration=1, total_price=150.00,
        status='confirmed'
    )
    
    # C. Completed Withdrawal (Withdrawn)
    Withdrawal.objects.create(
        user=teacher, amount=50.00, status='COMPLETED'
    )
    
    # D. Pending Withdrawal (Should NOT be in withdrawn_amount)
    Withdrawal.objects.create(
        user=teacher, amount=20.00, status='PENDING'
    )
    
    # 4. Call Earnings Endpoint
    view = CoachViewSet.as_view({'get': 'earnings'})
    request = factory.get('/api/v1/coach/earnings/')
    force_authenticate(request, user=teacher)
    response = view(request)
    
    print("GET Earnings Status:", response.status_code)
    print("Response Data:", response.data)
    
    # Expected:
    # earning: 100.00 (one completed session)
    # withdrawn: 50.00 (one completed withdrawal)
    # amount_expected: 150.00 (one confirmed future session)
    # Budget: 50.00 (100 - 50)
    
    data = response.data
    assert data['earning'] == 100.00
    assert data['withdrawn'] == 50.00
    assert data['amount_expected'] == 150.00
    assert data['Budget'] == 50.00
    assert len(data['response_obj']) >= 3 # session1, session2, withdrawal1
    
    print("--- Verification Successful! ---")

if __name__ == '__main__':
    run_tests()
