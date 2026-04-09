import pytest 
from event import Event
from datetime import date, time



def test_event_date():
    with pytest.raises(ValueError):
        first_event = Event(title="Test Title", date=date(2026, 2, 28), location="Test Location",
                       start_time=time(20,0), end_time=time(23,0),
                       organiser="Test Organiser", category="Test Category")
        
def test_event_times():
    with pytest.raises(ValueError):
        second_event = Event(title="Test Title", date=date(2026, 6, 28), location="Test Location",
                       start_time=time(20,0), end_time=time(3,0),
                       organiser="Test Organiser", category="Test Category")
        
def test_event_title():
    with pytest.raises(ValueError):
        third_event = Event(title=None, date=date(2026, 6, 28), location="Test Location",
                       start_time=time(20,0), end_time=time(23,0),
                       organiser="Test Organiser", category="Test Category")
        
def test_event_location():
    with pytest.raises(ValueError):
        fourth_event = Event(title="Test Title", date=date(2026, 6, 28), location=None,
                       start_time=time(20,0), end_time=time(23,0),
                       organiser="Test Organiser", category="Test Category")

def test_event_organiser():
    with pytest.raises(ValueError):
        fifth_event = Event(title="Test Title", date=date(2026, 6, 28), location="Test Location",
                       start_time=time(20,0), end_time=time(23,0),
                       organiser=None, category="Test Category")
        
def test_event_category():
    with pytest.raises(ValueError):
        sixth_event = Event(title="Test Title", date=date(2026, 6, 28), location="Test Location",
                       start_time=time(20,0), end_time=time(23,0),
                       organiser="Test Organiser", category=None)
        
        