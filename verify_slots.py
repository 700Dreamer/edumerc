import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth import get_user_model
from educoach.models import Coach, CoachingSession, CoachAvailabilityRange
from rest_framework.test import APIRequestFactory, force_authenticate
from educoach.views import CoachAvailabilityView, SmartSlotView, SessionViewSet

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
    print("--- Testing Coach Availability & Smart Booking ---")
    
    # 1. Setup Test Users
    teacher, _ = User.objects.get_or_create(username='test_teacher', email='t@test.com', role='TEACHER', is_coach=True)
    student, _ = User.objects.get_or_create(username='test_student', email='s@test.com', role='STUDENT')
    coach, _ = Coach.objects.get_or_create(user=teacher, defaults={'title': 'Math Expert', 'price_per_hour': 100})
    
    # Clear existing data
    CoachAvailabilityRange.objects.filter(coach=coach).delete()
    CoachingSession.objects.filter(coach=coach).delete()
    
    # 2. Test Availability PUT
    view = CoachAvailabilityView.as_view()
    data = {
        "weekly_schedule": [
            {
                "day_of_week": 1, # Monday
                "is_active": True,
                "ranges": [
                    {"start": "09:00", "end": "12:00"},
                    {"start": "14:00", "end": "17:00"}
                ]
            },
            {
                "day_of_week": 2, # Tuesday
                "is_active": False,
                "ranges": []
            } # other days will be defaulted
        ]
    }
    request = factory.put('/api/v1/coach/availability/', data, format='json')
    force_authenticate(request, user=teacher)
    response = view(request)
    print("PUT Availability Route Status:", response.status_code)
    
    # 3. Test Smart Slots GET
    view_slots = SmartSlotView.as_view()
    
    # Find next Monday
    today = datetime.now().date()
    days_ahead = 0 - today.weekday()
    if days_ahead <= 0: # Target next week
        days_ahead += 7
    next_monday = today + timedelta(days=days_ahead)
    
    request = factory.get(f'/api/v1/coach/tutors/{coach.id}/slots/?date={next_monday}&duration=2')
    response = view_slots(request, id=coach.id)
    print("GET Smart Slots (2 hours on Monday) Status:", response.status_code)
    print("Available Slots:", response.data.get('available_slots'))
    
    # 4. Test Session Booking (Atomic Check)
    view_book = SessionViewSet.as_view({'post': 'create'})
    book_data = {
        "tutor_id": coach.id,
        "date": str(next_monday),
        "time": "09:00",
        "duration": 2
    }
    request = factory.post('/api/v1/coach/sessions/', book_data, format='json')
    force_authenticate(request, user=student)
    response = view_book(request)
    print("POST Session Booking Status:", response.status_code)
    if response.status_code == 201:
        print("Booking successful! ID:", response.data.get('booking_id'))
        
    # Test Double Booking (Should Fail)
    request2 = factory.post('/api/v1/coach/sessions/', book_data, format='json')
    force_authenticate(request2, user=student)
    response2 = view_book(request2)
    print("POST Double Booking Status:", response2.status_code)
    if response2.status_code == 409:
        print("Double booking successfully prevented!")
        
    # Check slots again to see if 09:00 is removed and 10:00 is also removed or restricted
    request_slots2 = factory.get(f'/api/v1/coach/tutors/{coach.id}/slots/?date={next_monday}&duration=2')
    response_slots2 = view_slots(request_slots2, id=coach.id)
    print("Available Slots after booking:", response_slots2.data.get('available_slots'))
    
    print("--- Verification Complete ---")

if __name__ == '__main__':
    run_tests()
