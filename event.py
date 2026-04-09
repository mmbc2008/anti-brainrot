from dataclasses import dataclass, field
from datetime import date, time


@dataclass
class Event:
    title: str
    date: date
    location: str
    start_time: time
    end_time: time
    organiser: str
    category: str
    price: float = field(init=False, default=None)
    
    def __post_init__(self):
        if self.title is None:
            raise ValueError("Title cannot be empty.")
        if self.date < date.today():
            raise ValueError("Date cannot be in the past")
        if self.location is None:
            raise ValueError("Location cannot be empty.")
        if self.end_time < self.start_time:
            raise ValueError("End time cannot be before start time.")
        if self.organiser is None:
            raise ValueError("Organiser cannot be empty.")
        if self.category is None:
            raise ValueError("Category cannot be empty.")
        if self.price is not None and self.price < 0:
            raise ValueError("Price cannot be negative.")
    
        
        
    
    
    