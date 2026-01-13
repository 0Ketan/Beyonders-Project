"""
Availability Checker Module
This module contains functions to check faculty availability based on their teaching schedule.
"""

import json
from datetime import datetime


def load_json_file(filepath):
    """
    Load and return data from a JSON file.
    
    Args:
        filepath (str): Path to the JSON file
        
    Returns:
        list/dict: Parsed JSON data
    """
    try:
        with open(filepath, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: File {filepath} not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in {filepath}.")
        return []


def get_current_day_and_time():
    """
    Get the current day of the week and time.
    
    Returns:
        tuple: (day_name, current_time_str)
        Example: ("Monday", "14:30")
    """
    now = datetime.now()
    day_name = now.strftime("%A")  # Full day name (e.g., "Monday")
    current_time = now.strftime("%H:%M")  # 24-hour format (e.g., "14:30")
    return day_name, current_time


def is_time_in_range(current_time, start_time, end_time):
    """
    Check if current time falls within a given time range.
    
    Args:
        current_time (str): Current time in HH:MM format
        start_time (str): Start time in HH:MM format
        end_time (str): End time in HH:MM format
        
    Returns:
        bool: True if current time is within range, False otherwise
    """
    current = datetime.strptime(current_time, "%H:%M")
    start = datetime.strptime(start_time, "%H:%M")
    end = datetime.strptime(end_time, "%H:%M")
    
    return start <= current <= end


def check_faculty_availability(faculty_id, timetable_data):
    """
    Check if a faculty member is currently available.
    
    A faculty is NOT AVAILABLE if they are currently in a teaching period.
    Otherwise, they are AVAILABLE.
    
    Args:
        faculty_id (int): ID of the faculty member
        timetable_data (list): List of timetable entries
        
    Returns:
        dict: {
            'available': bool,
            'status': str (description of availability)
        }
    """
    current_day, current_time = get_current_day_and_time()
    
    # Find the faculty's schedule
    faculty_schedule = None
    for entry in timetable_data:
        if entry['faculty_id'] == faculty_id:
            faculty_schedule = entry['schedule']
            break
    
    # If no schedule found, assume available
    if not faculty_schedule:
        return {
            'available': True,
            'status': 'Available (No schedule found)'
        }
    
    # Check if current time falls within any teaching period
    for period in faculty_schedule:
        if period['day'] == current_day:
            if is_time_in_range(current_time, period['start_time'], period['end_time']):
                return {
                    'available': False,
                    'status': f'Currently in class ({period["start_time"]} - {period["end_time"]})'
                }
    
    # If not in any teaching period, faculty is available
    return {
        'available': True,
        'status': 'Available'
    }


def get_faculty_by_id(faculty_id, faculty_data):
    """
    Get faculty details by ID.
    
    Args:
        faculty_id (int): ID of the faculty member
        faculty_data (list): List of faculty entries
        
    Returns:
        dict: Faculty details or None if not found
    """
    for faculty in faculty_data:
        if faculty['id'] == faculty_id:
            return faculty
    return None


def get_faculty_by_name(faculty_name, faculty_data):
    """
    Get faculty details by name.
    
    Args:
        faculty_name (str): Name of the faculty member
        faculty_data (list): List of faculty entries
        
    Returns:
        dict: Faculty details or None if not found
    """
    for faculty in faculty_data:
        if faculty['name'] == faculty_name:
            return faculty
    return None
